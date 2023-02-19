"""Main start app file."""

import os
import pickle
from datetime import datetime

from bson.binary import Binary
from flask import Flask, Response, flash, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError

from camera_utils import generate_frames, get_face_id, take_screenshot_from_camera
from validation_schema import user_validation_schema


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", None)

connection_string = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(connection_string)
db = client.get_database("FaceID")
try:
    db.create_collection("users", validator=user_validation_schema)
except CollectionInvalid as e:
    print(e)
users = db.get_collection("users")
users.create_index("email", unique=True)


@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    """Index page."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        request.form.get("submit")
        return redirect(url_for("protected"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        screenshot = take_screenshot_from_camera(request.form.get("email"))
        # check whether screenshot file is saved
        if screenshot:
            face_id = get_face_id(screenshot)
            # check whether face recognition succeeded
            if len(face_id) != 0:
                try:
                    add_user = users.insert_one(
                        {
                            "email": request.form.get("email"),
                            "password": request.form.get("password"),
                            "image": f"user_screenshots/{request.form.get('email')}",
                            "face_id": Binary(pickle.dumps(face_id, protocol=2), subtype=128),
                            "date": datetime.utcnow(),
                        }
                    )
                    # check whether data inserting succeeded
                    if add_user:
                        return redirect(url_for("protected"))
                    flash("Error. Cannot save data to DB.")
                except DuplicateKeyError:
                    flash("The given email already exists.")

            else:
                flash("Cannot get face encoding, retake picture.")
        else:
            flash("Cannot find screenshot file.")
    return render_template("register.html")


@app.route("/take_screenshot", methods=["POST"])
def take_screenshot():
    return take_screenshot_from_camera("test")


@app.route("/protected")
def protected():
    return render_template("protected.html")


if __name__ == "__main__":
    app.run()
