from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from models.users import User
from bson.binary import Binary
from pyfingerprint.pyfingerprint import PyFingerprint
import pickle
import time
from time import sleep
from datetime import datetime
import pygame, os

#For testing only disable this if deploying
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize fingerprint f
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(f"Error initializing fingerprint f: {e}")

# Initialize pygame mixer
pygame.mixer.init(buffer=4096)

# Global variable to hold user data during the enrollment process
enrollment_data = {}

def start_fingerprint_enrollment(full_name, email, password):
    global enrollment_data

    try:
        # Store user data for later use
        enrollment_data = {
            "user_id": User.generate_user_id(),
            "full_name": full_name,
            "email": email,
            "password": password
        }

        print("Fingerprint f waiting for first scan...")
        # Load your MP3 file
        pygame.mixer.music.load("./sounds/f_waiting.mp3")
        pygame.mixer.music.play()

        time.sleep(.5)

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
            time.sleep(1)

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

        print("Fingerprint f waiting for second scan...")
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
            "user_id": User.generate_user_id(),
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


def check_fingerprint():
    """
    This function reads a fingerprint, searches for a match in the fingerprint f's memory,
    and returns the result including whether a match was found, the matching template position,
    and the accuracy score.

    Returns:
        tuple: (is_matched: bool, template_position: int, accuracy_score: int)
               is_matched is True if a match is found, False otherwise.
               template_position is the memory position of the matched fingerprint, -1 if no match.
               accuracy_score is the match score, 0 if no match.
    """
    try:
        sleep(1)
        # Initialize the fingerprint f (adjust the port and baud rate for your setup)
        f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The fingerprint f is protected by a password!')

        print(f'Currently stored fingers: {f.getTemplateCount()}/{f.getStorageCapacity()}')

        print('Waiting for finger...')

        # Wait for a finger to be placed and read by the f
        while f.readImage() == False:
            pass

        # Convert the read image to a template stored in charbuffer 1
        f.convertImage(0x01)

        # Search for a matching template in the f's memory
        result = f.searchTemplate()

        template_position = result[0]  # Position of the matched template in memory
        accuracy_score = result[1]     # Accuracy score of the match

        # If no match was found, template_position will be -1
        if template_position == -1:
            print('No match found!')
            return False, -1, 0  # No match, return -1 for template_position and 0 for accuracy_score

        else:
            print(f'Found template at position #{template_position}')
            print(f'The accuracy score is: {accuracy_score}')
            return True, template_position, accuracy_score

    except Exception as e:
        print(f'Operation failed! Exception message: {str(e)}')
        return False, -1, 0  # Return False for no match and 0 accuracy score on failure

    finally:
        # Wait 2 seconds before the next fingerprint read attempt
        sleep(2)