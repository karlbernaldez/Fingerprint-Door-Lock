"""Utilities to work with camera and face recognition."""

import os
from pathlib import Path

import cv2
import face_recognition as fr
import numpy as np


class Camera:
    """Class to work with a camera."""

    def __init__(self, device_number=0):
        self.device_number = device_number
        self.video_capture = cv2.VideoCapture(device_number)

    def generate_frames(self) -> bytes:
        """Generate frame by frame from the camera to embed it on a webpage."""
        while True:
            success, frame = self.take_screenshot_from_camera()
            if success:
                ret, buf = cv2.imencode(".jpg", frame)
                frame = buf.tobytes()
                yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            else:
                break

    def take_screenshot_from_camera(self) -> (bool, np.ndarray):
        """Take a screenshot from a camera."""
        success, frame = self.video_capture.read()
        return success, frame

    @staticmethod
    def save_screenshot_to_file(
        success: bool, frame: np.ndarray, username: str
    ) -> str | bool:
        """Save a screenshot to disk."""
        screenshots_folder = Path("static", "user_screenshots")
        screenshots_folder.mkdir(exist_ok=True)

        file_path = os.path.join(screenshots_folder, f"{username}.jpg")

        if success:
            _, buf = cv2.imencode(".jpg", frame)
            with open(file_path, "wb") as f:
                f.write(buf)
            return file_path
        return False

    def check_two_faces(self, known_face_encoding) -> bool:
        """Check if face encoding is the same as in the DB."""
        success, frame = self.take_screenshot_from_camera()
        if success:
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                new_face_encoding = fr.face_encodings(frame)[0]
                result = fr.compare_faces([known_face_encoding], new_face_encoding)

                return result[0]

            except IndexError:
                return False

    @staticmethod
    def get_face_encoding(frame) -> np.ndarray:
        """Create face encoding from camera frame."""
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_encoding = fr.face_encodings(frame)[0]
            return face_encoding.tolist()
        except (IndexError, AttributeError):
            return np.array([])
