import os
import pickle
from datetime import datetime
from bson import ObjectId
from bson.binary import Binary
from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify
)
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError
from werkzeug.security import check_password_hash, generate_password_hash
import serial
from validation_schema import user_validation_schema
import time
import serial
import board
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
from digitalio import DigitalInOut, Direction, Pull

app = Flask(__name__)
app.secret_key = os.urandom(24)

connection_string = os.getenv("MONGODB_URI", "mongodb+srv://fingerprint_db:admin1234@thesis.ro0a8.mongodb.net/?retryWrites=true&w=majority&appName=Thesis")
client = MongoClient(connection_string)
db = client.get_database("fingerprints")

# Initialize the fingerprint sensor
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    print("Fingerprint sensor initialized")
except Exception as e:
    print(f"Error initializing fingerprint sensor: {e}")

# Optional: Set up the touch pin (GPIO 17)
touch_pin = DigitalInOut(board.D17)
touch_pin.direction = Direction.INPUT
touch_pin.pull = Pull.UP

try:
    db.create_collection("fingerprints", validator=user_validation_schema)
except CollectionInvalid as e:
    print(e)

users = db.get_collection("fingerprints")
users.create_index("email", unique=True)

# ROUTES
@app.route("/")
def index():
    """Index page."""
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    """Index page."""
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log the user in using fingerprint sensor or email and password."""
    if request.method == "POST":
        session.pop("user", None)
        email = request.form.get("email")
        password = request.form.get("password")
        result = False

        user = users.find_one({"email": email})

        if not user:
            flash("User with this email does not exist.")
        elif user and password:
            result = check_password_hash(user["password"], password)
            print(result)
        elif user:
            if f.read_templates() >= 0:
                result = f.verify_model(pickle.loads(user["fingerprint_id"]))

        if result:
            session["user"] = user["email"]
            flash(f"Welcome, {user['email']}!")
            return redirect(url_for("profile", user_id=user["_id"]))
        else:
            flash("Wrong password or fingerprint does not match.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            full_name = request.form.get("full_name")
            email = request.form.get("email")
            password = request.form.get("password")

            print("Register form submitted")

            # Fingerprint enrollment process
            print("Waiting for finger...")
            while f.readImage() == False:
                pass

            # Convert image to characteristics
            f.convertImage(0x01)

            # Check if fingerprint is already registered
            result = f.searchTemplate()
            if result[0] >= 0:
                flash("Fingerprint already exists in the database.", "danger")
                return render_template("register.html")

            print("Remove your finger and place it again...")
            time.sleep(2)  # Allow time for the user to remove and re-place their finger

            # Wait for the second fingerprint scan
            while f.readImage() == False:
                pass

            # Convert the second image to characteristics
            f.convertImage(0x02)

            # Compare the characteristics of the two scans
            if f.compareCharacteristics() == 0:
                flash("Fingerprints do not match. Please try again.", "danger")
                return render_template("register.html")

            # Create a template and save it
            f.createTemplate()
            template_position = f.storeTemplate()

            # Store user information in MongoDB
            hashed_password = generate_password_hash(password)
            user_data = {
                "full_name": full_name,
                "email": email,
                "password": hashed_password,
                "fingerprint_id": Binary(pickle.dumps(f.downloadCharacteristics(0x01))),
                "template_position": template_position
            }

            users.insert_one(user_data)
            flash("User registered successfully.", "success")
            return redirect(url_for("login"))

        except DuplicateKeyError:
            flash("The given email already exists.", "danger")
        except Exception as error:
            app.logger.error(f"An error occurred while registering a user: {error}")
            flash("An error occurred while registering. Please try again later.", "danger")

    return render_template("register.html")

@app.route('/enroll-fingerprint', methods=['POST'])
def enroll_fingerprint():
    try:
        # Retrieve form data
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        message = "Fingerprints sensor waiting..."
        print(message)
        
        while f.readImage() == False:
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER1)

        result = f.searchTemplate()
        template_position = result[0]
        if template_position >= 0:
            message = f"This finger already exists at position #{template_position}."
            print(message)
            return jsonify({"status": "failed", "message": message}), 409

        message = "Remove finger..."
        print(message)
        time.sleep(2)

        while f.readImage() == False:
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER2)

        if f.compareCharacteristics() == 0:
            message = "Fingerprints do not match. Please try again."
            print(message)
            return jsonify({"status": "failed", "message": message}), 400

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
        users.insert_one(user_data)

        message = f"Finger enrolled successfully at position #{position_number}."
        print(message)
        return jsonify({"status": "success", "message": message, "position_number": position_number}), 201

    except DuplicateKeyError:
        message = "The given email already exists."
        print(message)
        return jsonify({"status": "failed", "message": message}), 409
    except Exception as e:
        message = f"Operation failed! Exception message: {e}"
        print(message)
        return jsonify({"status": "failed", "message": message}), 500


@app.route("/profile/<user_id>")
def profile(user_id):
    """User profile page."""
    if "user" in session:
        user = users.find_one(
            {"_id": ObjectId(user_id)}, {"email": 1, "date": 1}
        )
        return render_template("profile.html", user=user)
    flash("You are not logged in.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
