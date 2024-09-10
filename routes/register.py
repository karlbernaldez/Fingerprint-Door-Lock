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
    print("Received request at /register") 
    # if request.method == "POST":
    #     try:
    #         full_name = request.form.get("full_name")
    #         email = request.form.get("email")
    #         password = request.form.get("password")
    #         print(f"Form data: {full_name}, {email}, {password}")
            
    #         # Example response without database operations
    #         flash("User registration simulated successfully.", "success")
    #         return redirect(url_for("routes.login"))
    #     except Exception as error:
    #         print(f"An error occurred: {error}")
    #         flash(f"An error occurred: {error}", "danger")
    return render_template("register.html")