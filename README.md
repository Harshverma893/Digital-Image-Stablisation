Digital Image Stabilization
A Flask-based web application for video stabilization using OpenCV, designed to reduce jitter by 80% in both uploaded videos and live camera feeds. Featuring a user-friendly interface, real-time processing, and low-latency performance, this project is ideal for stabilizing dynamic scenes in computer vision applications. An optional executable version is available for standalone use.
Features

Jitter Reduction: Achieves 80% reduction in video jitter using OpenCV’s stabilization algorithms.
Real-Time Stabilization: Processes live camera feeds with optimized low-latency performance.
Web-Based Interface: Upload videos or stabilize live feeds via a modern, responsive UI.
Responsive Design: Built with Tailwind CSS for a clean, mobile-friendly experience.
Executable Support: Optional .exe version for standalone deployment (Windows).

Technologies

Backend: Flask, Python, OpenCV
Frontend: HTML, JavaScript, Tailwind CSS
Libraries: numpy, imutils, flask
Camera: Supports webcam or IP camera for live feeds

Setup Instructions
Prerequisites

Python 3.8 or higher
Git
Webcam or IP camera (for live stabilization)
Administrative access for camera permissions

Installation

Clone the repository:git clone https://github.com/Harshverma893/Digital-Image-Stabilization.git
cd Digital-Image-Stabilization


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install flask opencv-python numpy imutils


Run the application:python app.py


Access the app

