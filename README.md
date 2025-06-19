
# 🎯 Digital Image Stabilization

A Flask-based web application for video stabilization using OpenCV, designed to reduce jitter by up to **80%** in both uploaded videos and live camera feeds. Featuring a user-friendly interface, real-time processing, and low-latency performance, this project is ideal for stabilizing dynamic scenes in computer vision applications. An optional executable version is available for standalone use on Windows.

---

## ✨ Features

- **Jitter Reduction:** Achieves up to 80% reduction in video jitter using OpenCV’s stabilization algorithms.
- **Live Feed Support:** Real-time video stabilization using webcam or IP camera.
- **Upload & Stabilize:** Upload a jittery video and download a stabilized version with automatic cropping.
- **Responsive Web Interface:** Upload videos or stabilize live feeds via a modern UI.
- **Executable Support:** Optional `.exe` version for standalone deployment on Windows.

---

## 🛠️ Technologies Used

- **Languages:** Python
- **Libraries:** OpenCV, NumPy, Flask, Imutils
- **Frontend:**  HTML, JavaScript, CSS
- **Video Processing:** Optical Flow, RANSAC, Smoothing Filters
- **Deployment:** Flask-based local web app

---

## 🚀 Demo Videos

### 🔴 Live Video Stabilization Demo
[![Live Video Stabilization](https://img.youtube.com/vi/ktRut3g8Xww/0.jpg)](https://youtu.be/ktRut3g8Xww)

### 🎞️ Comparison: Before & After Stabilization

#### Set 1
| Before Stabilization | After Stabilization |
|----------------------|---------------------|
| [![Before](https://img.youtube.com/vi/E-ot4VLXLI8/0.jpg)](https://youtu.be/E-ot4VLXLI8) | [![After](https://img.youtube.com/vi/GS7vr0KGZbs/0.jpg)](https://youtu.be/GS7vr0KGZbs) |

#### Set 2
| Before Stabilization | After Stabilization |
|----------------------|---------------------|
| [![Before](https://img.youtube.com/vi/EF9Q2IY1-RU/0.jpg)](https://youtu.be/EF9Q2IY1-RU) | [![After](https://img.youtube.com/vi/WvNeM-nW6P4/0.jpg)](https://youtu.be/WvNeM-nW6P4) |

---

## 🔧 Installation & Setup

### 📦 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git
- A webcam or IP camera for live mode

### 📁 Clone the Repository

```bash
git clone https://github.com/Harshverma893/Digital-Image-Stabilization.git
cd Digital-Image-Stabilization
```

### 🧪 Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📚 Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```bash
pip install flask opencv-python numpy imutils
```

---

## ▶️ Run the App

### 📹 For Live Camera Stabilization

```bash
python live_stabilization.py
```

- Visit: [http://localhost:5000](http://localhost:5000)
- See side-by-side comparison of live camera stabilization

### 🎞️ For Uploaded Video Stabilization

```bash
python app.py
```

- Upload a shaky `.mp4` file and download a stabilized version

---

## 📦 Optional: Build Standalone Executable (Windows)

To build an executable for easy deployment:

```bash
pip install pyinstaller
pyinstaller --onefile app.py
```

---

## 📬 Contact

Created by **Harsh Verma**  
GitHub: [Harshverma893](https://github.com/Harshverma893)  
Email: harshvij02@gmail.com

---

## 📄 License

MIT License

Copyright (c) 2025 Harsh Verma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

