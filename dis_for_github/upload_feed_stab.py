#this isgood but the qality is not goood 
from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

SMOOTHING_RADIUS = 100

def movingAverage(curve, radius):
    window_size = 2 * radius + 1
    f = np.ones(window_size)/window_size
    curve_pad = np.pad(curve, (radius, radius), mode='edge')
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    return curve_smoothed[radius:-radius]

def smooth(trajectory):
    smoothed_trajectory = np.copy(trajectory)
    for i in range(3):
        smoothed_trajectory[:, i] = movingAverage(trajectory[:, i], radius=SMOOTHING_RADIUS)
    return smoothed_trajectory

def fixBorder(frame):
    s = frame.shape
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.04)
    frame = cv2.warpAffine(frame, T, (s[1], s[0]))
    return frame

def crop_black_borders(video_path, output_path, crop_x, crop_y, crop_w, crop_h):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, fourcc, fps, (crop_w, crop_h))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Ensure crop coordinates are within frame dimensions
        y1 = max(crop_y, 0)
        y2 = min(crop_y + crop_h, frame.shape[0])
        x1 = max(crop_x, 0)
        x2 = min(crop_x + crop_w, frame.shape[1])
        cropped_frame = frame[y1:y2, x1:x2]
        
        # Handle edge cases where crop might be slightly out of bounds
        if cropped_frame.shape[0] != crop_h or cropped_frame.shape[1] != crop_w:
            cropped_frame = cv2.resize(cropped_frame, (crop_w, crop_h))
        
        out.write(cropped_frame)
    
    cap.release()
    out.release()

def stabilize_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_output = output_path.replace('.mp4', '_temp.mp4')
    out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))
    
    # Initialize crop parameters
    global_max_left = 0
    global_max_top = 0
    global_min_right = width
    global_min_bottom = height

    # Read first frame
    _, prev = cap.read()
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    transforms = np.zeros((n_frames - 1, 3), np.float32)

    # Calculate transforms
    for i in range(n_frames - 2):
        prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)
        succ, curr = cap.read()
        if not succ:
            break
        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
        curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)
        prev_pts = prev_pts[status == 1]
        curr_pts = curr_pts[status == 1]
        m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)
        dx, dy, da = m[0,2], m[1,2], np.arctan2(m[1,0], m[0,0])
        transforms[i] = [dx, dy, da]
        prev_gray = curr_gray
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Smooth transforms
    smoothed_trajectory = smooth(np.cumsum(transforms, axis=0))
    transforms_smooth = transforms + (smoothed_trajectory - np.cumsum(transforms, axis=0))

    # Apply stabilization and collect crop parameters
    for i in range(n_frames - 2):
        success, frame = cap.read()
        if not success:
            break
        
        dx, dy, da = transforms_smooth[i]
        m = np.array([[np.cos(da), -np.sin(da), dx], 
                      [np.sin(da), np.cos(da), dy]], dtype=np.float32)
        
        frame_stabilized = cv2.warpAffine(frame, m, (width, height))
        frame_stabilized = fixBorder(frame_stabilized)
        
        # Update crop parameters
        gray = cv2.cvtColor(frame_stabilized, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        x, y, w, h = cv2.boundingRect(thresh)
        
        current_right = x + w
        current_bottom = y + h
        
        global_max_left = max(global_max_left, x)
        global_max_top = max(global_max_top, y)
        global_min_right = min(global_min_right, current_right)
        global_min_bottom = min(global_min_bottom, current_bottom)
        
        out.write(frame_stabilized)
    
    cap.release()
    out.release()

    # Calculate final crop dimensions
    crop_x = global_max_left
    crop_y = global_max_top
    crop_w = max(global_min_right - crop_x, 1)
    crop_h = max(global_min_bottom - crop_y, 1)
    
    # Apply final crop
    crop_black_borders(temp_output, output_path, crop_x, crop_y, crop_w, crop_h)
    os.remove(temp_output)

def iterative_stabilize_video(video_path, output_path, max_iterations=2):
    for _ in range(max_iterations):
        stabilize_video(video_path, output_path)
        # Use the output of the current stabilization as the input for the next iteration
        video_path = output_path

    # Final stabilization and cropping
    stabilize_video(output_path, output_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(OUTPUT_FOLDER, 'stabilized_' + file.filename)
            file.save(input_path)
            stabilize_video(input_path, output_path)
            return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)