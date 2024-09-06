from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from models.users import User
from bson.binary import Binary
from pyfingerprint.pyfingerprint import PyFingerprint
import pickle
import time
from datetime import datetime

# Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(f"Error initializing fingerprint sensor: {e}")

def enroll_fingerprint(full_name, email, password):
    try:
        # Initialize the fingerprint sensor
        print("Fingerprint sensor waiting...")
        
        while not f.readImage():
            pass

        f.convertImage(0x01)

        result = f.searchTemplate()
        template_position = result[0]
        if template_position >= 0:
            message = f"This finger already exists at position #{template_position}."
            print(message)
            return {"status": "failed", "message": message}, 409

        print("Remove finger and place it again...")
        time.sleep(2)

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
        hashed_password = generate_password_hash(password)
        user_data = {
            "full_name": full_name,
            "email": email,
            "password": hashed_password,
            "fingerprint_id": Binary(pickle.dumps(f.downloadCharacteristics(0x01))),
            "template_position": position_number,
            "date": datetime.utcnow()
        }

        # Store user information in MongoDB
        User(**user_data).save()

        message = f"Finger enrolled successfully at position #{position_number}."
        print(message)
        return {"status": "success", "message": message, "position_number": position_number}, 201

    except DuplicateKeyError:
        message = "The given email already exists."
        print(message)
        return {"status": "failed", "message": message}, 409
    except Exception as e:
        message = f"Operation failed! Exception message: {e}"
        print(message)
        return {"status": "failed", "message": message}, 500
