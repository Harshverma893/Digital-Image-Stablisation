
# 🎯 Digital Image Stabilization

A Flask-based web application for video stabilization using OpenCV, designed to reduce jitter by up to **80%** in both uploaded videos and live camera feeds. Featuring a user-friendly interface, real-time processing, and low-latency performance, this project is ideal for stabilizing dynamic scenes in computer vision applications. An optional executable version is available for standalone use on Windows.

---

## ✨ Features

- **Jitter Reduction:** Achieves up to 80% reduction in video jitter using OpenCV’s stabilization algorithms.
- **Real-Time Stabilization:** Processes live camera feeds with optimized low-latency performance using CUDA (GPU acceleration).
- **Web-Based Interface:** Upload videos or stabilize live feeds via a modern, responsive UI.
- **Executable Support:** Optional `.exe` version for standalone deployment on Windows.

---

## 🛠️ Technologies

- **Backend:** Flask, Python, OpenCV
- **Frontend:** HTML, JavaScript, Tailwind CSS
- **GPU Acceleration:** CUDA
- **Libraries:** numpy, imutils, flask
- **Camera Input:** Supports USB webcam or IP camera

---

## 🚀 Demo Videos

### 🔴 Live Video Stabilization Demo
[![Live Video Stabilization](https://img.youtube.com/vi/ktRut3g8Xww/0.jpg)](https://youtu.be/ktRut3g8Xww)

---

### 🎞️ Comparison: Recorded Video Before & After Stabilization

#### 📁 Set 1

| Before Stabilization | After Stabilization |
|----------------------|---------------------|
| [![Before](https://img.youtube.com/vi/E-ot4VLXLI8/0.jpg)](https://youtu.be/E-ot4VLXLI8) | [![After](https://img.youtube.com/vi/GS7vr0KGZbs/0.jpg)](https://youtu.be/GS7vr0KGZbs) |

#### 📁 Set 2

| Before Stabilization | After Stabilization |
|----------------------|---------------------|
| [![Before](https://img.youtube.com/vi/EF9Q2IY1-RU/0.jpg)](https://youtu.be/EF9Q2IY1-RU) | [![After](https://img.youtube.com/vi/WvNeM-nW6P4/0.jpg)](https://youtu.be/WvNeM-nW6P4) |

---

## 🧰 Setup Instructions

### 🔧 Prerequisites

- Python 3.8 or higher
- Git
- Webcam or IP camera (for live stabilization)
- Admin access for camera permissions (if required)

---

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Harshverma893/Digital-Image-Stabilization.git
   cd Digital-Image-Stabilization
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**
   ```bash
   pip install flask opencv-python numpy imutils
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   Open your browser and go to:  
   `http://localhost:5000`

---

## 📦 Optional: Executable Version

If you want to run the project as a standalone `.exe` on Windows, a packaged version is available. Instructions for building it with `pyinstaller` or downloading a prebuilt `.exe` can be provided in the Releases section (coming soon).

---

## 📬 Contact

Created by **Harsh Verma**  
GitHub: [Harshverma893](https://github.com/Harshverma893)  
Email: harshvij02@gmail.com

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
