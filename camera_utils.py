"""Utilities to work with camera and face recognition."""

from pathlib import Path

import cv2
import face_recognition as fr
import numpy as np

# camera = cv2.VideoCapture(0)


class Camera:
    """Class to work with a camera."""

    def __init__(self, device_number=0):
        self.device_number = device_number
        self.video_capture = cv2.VideoCapture(device_number)

    def generate_frames(self):
        """Generate frame by frame from the camera to embed it on a webpage."""
        while True:
            success, frame = self.video_capture.read()
            if success:
                ret, buf = cv2.imencode(".jpg", frame)
                frame = buf.tobytes()
                yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            else:
                break

    def take_screenshot_from_camera(self, username: str) -> str | bool:
        """Take a screenshot from a webcam and save it to disk."""
        screenshots_folder = Path("user_screenshots")
        screenshots_folder.mkdir(exist_ok=True)

        file_path = f"{screenshots_folder}/{username}.jpg"

        success, frame = self.video_capture.read()
        if success:
            _, buf = cv2.imencode(".jpg", frame)
            with open(file_path, "wb") as f:
                f.write(buf)
            return file_path
        return False

    def check_face(self, known_face_encoding) -> bool:
        """Check if face encoding is the same as in the DB."""
        success, frame = self.video_capture.read()
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

    @staticmethod
    def get_face_encoding(img_file: str) -> np.ndarray:
        """Create face encoding from image on a disk."""
        try:
            image = fr.load_image_file(img_file)
            face_encoding = fr.face_encodings(image)[0]
            return face_encoding.tolist()
        except (IndexError, AttributeError):
            return np.array([])
