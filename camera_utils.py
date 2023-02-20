"""Utilities to work with camera and face recognition."""

from pathlib import Path

import cv2
import face_recognition as fr
import numpy as np

camera = cv2.VideoCapture(0)


def check_face(known_face_encoding) -> bool:
    """Check if face encoding is the same as in the DB."""
    success, frame = camera.read()
    if success:
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            new_face_encoding = fr.face_encodings(frame)[0]
            result = fr.compare_faces([known_face_encoding], new_face_encoding)

            if not all(result):
                return False
            return True
        except IndexError:
            return False


def get_face_id(img_file: str) -> list[np.ndarray]:
    """Create face encoding from image on a disk."""
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
