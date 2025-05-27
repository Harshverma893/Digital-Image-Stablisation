#better than ver3
from flask import Flask, Response, render_template
import cv2
import time
import os
import numpy as np

app = Flask(__name__)

SMOOTHING_RADIUS = 10  # Increased for better smoothing
CROP_FACTOR = 0.99      # Crop 10% from each border

def moving_average(curve, radius):
    window_size = radius + 1
    if len(curve) < window_size:
        return np.mean(curve, axis=0)
    return np.mean(curve[-window_size:], axis=0)

def fix_border(frame):
    s = frame.shape
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.04)
    return cv2.warpAffine(frame, T, (s[1], s[0]))

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open video source")

    # Initialize stabilization variables
    prev_gray = None
    transforms = []
    cumulative_trajectory = np.zeros((0, 3))
    smoothed_trajectory = np.zeros((0, 3))
    
    # Get video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate fixed crop dimensions
    crop_w = int(width * CROP_FACTOR)
    crop_h = int(height * CROP_FACTOR)
    crop_x = (width - crop_w) // 2
    crop_y = (height - crop_h) // 2

    while True:
        start_time = time.time()
        success, frame = cap.read()
        if not success:
            break

        unstabilized_cropped = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
        unstabilized = cv2.resize(unstabilized_cropped, (width, height), 
                                interpolation=cv2.INTER_LANCZOS4)

        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stabilized_frame = frame.copy()

        if prev_gray is not None:
            # Detect features with higher quality and more points
            prev_pts = cv2.goodFeaturesToTrack(prev_gray, 
                                             maxCorners=500,
                                             qualityLevel=0.05,
                                             minDistance=10,
                                             blockSize=3)
            
            if prev_pts is not None:
                # Calculate optical flow with improved parameters
                curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
                    prev_gray, current_gray, prev_pts, None,
                    winSize=(21, 21),
                    maxLevel=3,
                    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
                )
                
                if curr_pts is not None:
                    valid_pts = status.squeeze().astype(bool)
                    prev_pts = prev_pts[valid_pts]
                    curr_pts = curr_pts[valid_pts]

                    if len(prev_pts) >= 4 and len(curr_pts) >= 4:
                        # Estimate affine transformation with RANSAC and check inliers
                        m, inliers = cv2.estimateAffinePartial2D(
                            prev_pts, curr_pts,
                            method=cv2.RANSAC,
                            ransacReprojThreshold=1.0
                        )
                        
                        if m is not None:
                            num_inliers = np.sum(inliers)
                            if num_inliers < 10:  # Threshold for inliers
                                dx, dy, da = 0, 0, 0
                            else:
                                dx = m[0, 2]
                                dy = m[1, 2]
                                da = np.arctan2(m[1, 0], m[0, 0])
                        else:
                            dx, dy, da = 0, 0, 0
                    else:
                        dx, dy, da = 0, 0, 0
                else:
                    dx, dy, da = 0, 0, 0
            else:
                dx, dy, da = 0, 0, 0

            transforms.append([dx, dy, da])
            
            if cumulative_trajectory.size == 0:
                cumulative_trajectory = np.array([[dx, dy, da]])
            else:
                new_entry = cumulative_trajectory[-1] + np.array([dx, dy, da])
                cumulative_trajectory = np.vstack([cumulative_trajectory, new_entry])

            # Smooth trajectory with increased radius
            if len(cumulative_trajectory) > 1:
                smoothed = []
                for i in range(len(cumulative_trajectory)):
                    start = max(0, i - SMOOTHING_RADIUS)
                    window = cumulative_trajectory[start:i+1]
                    smoothed.append(np.mean(window, axis=0))
                smoothed_trajectory = np.array(smoothed)

                current_index = len(cumulative_trajectory) - 1
                adjustment = smoothed_trajectory[current_index] - cumulative_trajectory[current_index]
                adj_dx, adj_dy, adj_da = adjustment

                m = np.array([
                    [np.cos(adj_da), -np.sin(adj_da), adj_dx],
                    [np.sin(adj_da),  np.cos(adj_da), adj_dy]
                ], dtype=np.float32)

                stabilized_frame = cv2.warpAffine(frame, m, (width, height))
                # stabilized_frame = cv2.warpAffine(frame, m, (width, height),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)

                # Comment out fix_border if unnecessary
                # stabilized_frame = fix_border(stabilized_frame)

        # Apply crop to stabilized frame
        stabilized_cropped = stabilized_frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
        stabilized = cv2.resize(stabilized_cropped, (width, height), 
                              interpolation=cv2.INTER_LANCZOS4)

        # Combine frames side by side
        combined = cv2.hconcat([unstabilized, stabilized])
        cv2.putText(combined, "Unstabilized", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(combined, "Stabilized", (width + 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # Calculate and display FPS
        process_time = time.time() - start_time
        fps = 1.0 / process_time if process_time > 0 else 0
        cv2.putText(combined, f"FPS: {fps:.2f}", (width + 10, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
 
        ret, buffer = cv2.imencode('.jpg', combined)
        if not ret:
            continue
 
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')

        prev_gray = current_gray

    cap.release()

@app.route('/')
def index():
    return render_template('live.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)