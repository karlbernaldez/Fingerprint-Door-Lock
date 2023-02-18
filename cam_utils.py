"""."""

import os

import cv2

camera = cv2.VideoCapture(0)


def take_screenshot_from_camera(username: str):
    """Take a screenshot from a webcam and save it to disk."""
    if not os.path.exists("user_screenshots"):
        os.mkdir("user_screenshots")

    success, frame = camera.read()
    if success:
        cv2.imwrite(f"{username}.jpg", frame)
        print("Screenshot saved to disk.")
        ret, buf = cv2.imencode(".jpg", frame)
        frame = buf.tobytes()
        return frame
    return None


def generate_frames():
    """ "Generate frame by frame from camera."""
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buf = cv2.imencode(".jpg", frame)
            frame = buf.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
