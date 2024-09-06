from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from . import routes
from models.users import User
import pickle
from bson.binary import Binary
from pyfingerprint.pyfingerprint import PyFingerprint
import time
from datetime import datetime

# Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print(f"Error initializing fingerprint sensor: {e}")

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pass
        # try:
        #     full_name = request.form.get("full_name")
        #     email = request.form.get("email")
        #     password = request.form.get("password")
        #     # Handle fingerprint enrollment
        #     # ...
        #     hashed_password = generate_password_hash(password)
        #     user_data = {
        #         "full_name": full_name,
        #         "email": email,
        #         "password": hashed_password,
        #         "fingerprint_id": Binary(pickle.dumps(f.downloadCharacteristics(0x01))),
        #         "template_position": template_position,
        #         "date": datetime.utcnow()
        #     }
        #     User(**user_data).save()
        #     flash("User registered successfully.", "success")
        #     return redirect(url_for("routes.login"))
        # except DuplicateKeyError:
        #     flash("The given email already exists.", "danger")
        # except Exception as error:
        #     flash(f"An error occurred: {error}", "danger")
    return render_template("register.html")
