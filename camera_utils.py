"""."""

from pathlib import Path

import cv2
import face_recognition as fr
from numpy import ndarray


camera = cv2.VideoCapture(0)


def get_face_id(img_file: str) -> list[ndarray]:
    """Create face encoding."""
    try:
        image = fr.load_image_file(img_file)
        face_id = fr.face_encodings(image)[0]
        return face_id.tolist()
    except (IndexError, AttributeError):
        return []


def take_screenshot_from_camera(username: str) -> str | bool:
    """Take a screenshot from a webcam and save it to disk."""
    screenshots_folder = Path("user_screenshots")
    screenshots_folder.mkdir(exist_ok=True)

    file_path = f"{screenshots_folder}/{username}.jpg"

    success, frame = camera.read()
    if success:
        _, buf = cv2.imencode(".jpg", frame)
        with open(file_path, "wb") as f:
            f.write(buf)
        return file_path
    return False


def generate_frames():
    """Generate frame by frame from the camera to embed it on a webpage."""
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buf = cv2.imencode(".jpg", frame)
            frame = buf.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
