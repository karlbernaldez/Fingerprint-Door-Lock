from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from models.users import User
from bson.binary import Binary
from pyfingerprint.pyfingerprint import PyFingerprint
import pickle
import time
from datetime import datetime
import pygame

# Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(f"Error initializing fingerprint sensor: {e}")

# Initialize pygame mixer
pygame.mixer.init(buffer=4096)

# Global variable to hold user data during the enrollment process
enrollment_data = {}

def start_fingerprint_enrollment(full_name, email, password):
    global enrollment_data

    try:
        # Store user data for later use
        enrollment_data = {
            "full_name": full_name,
            "email": email,
            "password": password
        }

        print("Fingerprint sensor waiting for first scan...")
        # Load your MP3 file
        pygame.mixer.music.load("./sounds/sensor_waiting.mp3")
        pygame.mixer.music.play()

        while not f.readImage():
            pass

        f.convertImage(0x01)

        result = f.searchTemplate()
        template_position = result[0]
        if template_position >= 0:
            message = f"This finger already exists at position #{template_position}."
            
            # Load your MP3 file
            pygame.mixer.music.load("./sounds/already_exists.mp3")
            pygame.mixer.music.play()
            
            print(message)
            return {"status": "failed", "message": message}, 409

        print("First scan successful. Please remove your finger and proceed with the second scan.")
        # Load your MP3 file
        pygame.mixer.music.load("./sounds/first_success.mp3")
        pygame.mixer.music.play()
        return {"status": "success", "message": "First scan complete. Proceed with the second scan."}, 200

    except Exception as e:
        message = f"Operation failed! Exception message: {e}"
        print(message)
        return {"status": "failed", "message": message}, 500

def complete_fingerprint_enrollment():
    global enrollment_data
    time.sleep(2)
    try:
        # Ensure user data is available
        if not enrollment_data:
            message = "No enrollment data found. Please start the enrollment process."
            return {"status": "failed", "message": message}, 400

        print("Fingerprint sensor waiting for second scan...")
        # Load your MP3 file
        pygame.mixer.music.load("./sounds/second_scan.mp3")
        pygame.mixer.music.play()
        while not f.readImage():
            pass

        f.convertImage(0x02)

        if f.compareCharacteristics() == 0:
            message = "Fingerprints do not match. Please try again."
            print(message)
            return {"status": "failed", "message": message}, 400

        f.createTemplate()
        position_number = f.storeTemplate()

        # Hash the password and prepare the user data
        hashed_password = generate_password_hash(enrollment_data["password"])
        user_data = {
            "full_name": enrollment_data["full_name"],
            "email": enrollment_data["email"],
            "password": hashed_password,
            "fingerprint_id": Binary(pickle.dumps(f.downloadCharacteristics(0x01))),
            "template_position": position_number,
            "date": datetime.utcnow()
        }

        # Store user information in MongoDB
        User(**user_data).save()

        message = f"Fingerprint enrolled successfully at position #{position_number}."
        # Load your MP3 file
        pygame.mixer.music.load("./sounds/sucess.mp3")
        pygame.mixer.music.play()
        print(message)

        # Clear the enrollment data
        enrollment_data = {}

        return {"status": "success", "message": message, "position_number": position_number}, 201

    except DuplicateKeyError:
        message = "The given email already exists."
        print(message)
        return {"status": "failed", "message": message}, 409
    except Exception as e:
        message = f"Operation failed! Exception message: {e}"
        print(message)
        return {"status": "failed", "message": message}, 500
