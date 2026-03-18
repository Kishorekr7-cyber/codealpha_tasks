"""
CodeAlpha Internship - Task 4: Object Detection and Tracking
Uses YOLOv8 (ultralytics) for detection + built-in ByteTrack for tracking.
Supports: webcam, video file, or image file.

Install: pip install ultralytics opencv-python
"""

import cv2
import argparse
import sys
from pathlib import Path
from ultralytics import YOLO

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_NAME   = "yolov8n.pt"   # nano — fast; swap for yolov8s.pt / yolov8m.pt for more accuracy
CONFIDENCE   = 0.4            # Minimum detection confidence
IOU_THRESH   = 0.45           # IoU threshold for NMS
WINDOW_TITLE = "CodeAlpha — Object Detection & Tracking (press Q to quit)"

# Pretty colour palette (BGR) cycled by tracking ID
COLORS = [
    (255, 87,  34),   # Deep Orange
    ( 33, 150, 243),  # Blue
    ( 76, 175,  80),  # Green
    (156,  39, 176),  # Purple
    (255, 193,   7),  # Amber
    (  0, 188, 212),  # Cyan
    (233,  30,  99),  # Pink
    (121, 85,  72),   # Brown
]

def get_color(track_id: int):
    return COLORS[int(track_id) % len(COLORS)]

# ── Core processing ───────────────────────────────────────────────────────────
def process_source(source, model: YOLO, save_output: bool = False):
    """
    Run detection + tracking on a webcam, video file, or image.
    source: 0 (webcam) | "path/to/video.mp4" | "path/to/image.jpg"
    """
    is_image = isinstance(source, str) and Path(source).suffix.lower() in {
        ".jpg", ".jpeg", ".png", ".bmp", ".webp"
    }

    if is_image:
        _process_image(source, model)
    else:
        _process_video(source, model, save_output)


def _draw_box(frame, box, track_id, label: str, conf: float):
    x1, y1, x2, y2 = map(int, box)
    color = get_color(track_id)

    # Bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Label background
    text = f"#{track_id} {label} {conf:.0%}"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
    cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)

    # Label text
    cv2.putText(frame, text, (x1 + 3, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)


def _annotate_frame(frame, results):
    """Parse YOLO results and draw boxes on frame."""
    count = 0
    for r in results:
        boxes = r.boxes
        if boxes is None:
            continue
        for box in boxes:
            conf  = float(box.conf[0])
            cls   = int(box.cls[0])
            label = r.names[cls]
            tid   = int(box.id[0]) if box.id is not None else 0
            _draw_box(frame, box.xyxy[0], tid, label, conf)
            count += 1

    # Object count overlay
    cv2.putText(frame, f"Objects: {count}", (12, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 200), 2, cv2.LINE_AA)
    return frame


def _process_video(source, model: YOLO, save_output: bool):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {source}")
        sys.exit(1)

    w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    writer = None
    if save_output:
        out_path = "output_tracked.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
        print(f"[INFO] Saving output to: {out_path}")

    print("[INFO] Running… Press Q in the window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Tracking (persist=True keeps IDs across frames)
        results = model.track(
            frame,
            persist=True,
            conf=CONFIDENCE,
            iou=IOU_THRESH,
            verbose=False,
        )

        frame = _annotate_frame(frame, results)

        cv2.imshow(WINDOW_TITLE, frame)
        if writer:
            writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("[INFO] Done.")


def _process_image(path: str, model: YOLO):
    frame = cv2.imread(path)
    if frame is None:
        print(f"[ERROR] Cannot read image: {path}")
        sys.exit(1)

    results = model(frame, conf=CONFIDENCE, iou=IOU_THRESH, verbose=False)
    # For images assign sequential IDs (no real tracking needed)
    for r in results:
        if r.boxes is not None:
            for i, box in enumerate(r.boxes):
                box.id = [i + 1]  # type: ignore

    frame = _annotate_frame(frame, results)

    out_path = "output_detected.jpg"
    cv2.imwrite(out_path, frame)
    print(f"[INFO] Result saved to {out_path}")

    cv2.imshow(WINDOW_TITLE, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ── CLI ───────────────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="CodeAlpha Task 4 — YOLO Object Detection & Tracking"
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Input source: 0 = webcam, path to video file, or path to image",
    )
    parser.add_argument(
        "--model",
        default=MODEL_NAME,
        help="YOLO model weights (default: yolov8n.pt)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save annotated output video to output_tracked.mp4",
    )
    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = parse_args()

    # Convert "0" string to int for webcam
    source = int(args.source) if args.source.isdigit() else args.source

    print(f"[INFO] Loading model: {args.model}")
    model = YOLO(args.model)
    print(f"[INFO] Model loaded. Source: {source}")

    process_source(source, model, save_output=args.save)
