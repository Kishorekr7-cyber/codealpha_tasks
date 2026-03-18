# 🎯 Object Detection & Tracking — CodeAlpha AI Internship Task 4

Real-time object detection and tracking using **YOLOv8** + **ByteTrack**, powered by the `ultralytics` library.

## Features
- Real-time detection on webcam or video file
- Per-object tracking with persistent IDs across frames
- Coloured bounding boxes and labels with confidence scores
- Live object count overlay
- Image detection support
- Optional save to output video file

## Setup & Run

```bash
# 1. Install dependencies
pip install ultralytics opencv-python

# 2a. Run with webcam (default)
python detect_track.py

# 2b. Run with a video file
python detect_track.py --source path/to/video.mp4

# 2c. Run with an image
python detect_track.py --source path/to/image.jpg

# 2d. Save the output video
python detect_track.py --source path/to/video.mp4 --save

# 2e. Use a larger (more accurate) model
python detect_track.py --model yolov8s.pt
```

Press **Q** to quit.

## How It Works
1. **YOLOv8** detects objects in every frame (80 COCO classes: person, car, dog, etc.)
2. **ByteTrack** (built into ultralytics) assigns persistent IDs to tracked objects
3. Bounding boxes, labels, confidence scores, and track IDs are drawn on screen
4. Press Q to stop

## Model Options (auto-downloaded on first run)
| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| yolov8n.pt | 6MB | ⚡ Fastest | Good |
| yolov8s.pt | 22MB | Fast | Better |
| yolov8m.pt | 50MB | Medium | Best for CPU |

## Tech Stack
- **Python 3.x**
- **Ultralytics YOLOv8** — detection + ByteTrack tracking
- **OpenCV** — video capture and rendering

## Project Structure
```
CodeAlpha_ObjectDetectionTracking/
├── detect_track.py   # Main script
├── requirements.txt  # Dependencies
└── README.md
```
