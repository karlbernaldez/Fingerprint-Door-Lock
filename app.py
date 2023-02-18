"""Main start app file."""

import os
from datetime import datetime

from flask import Flask, Response, redirect, render_template, request
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from cam_utils import generate_frames
from validation_schema import user_validation_schema

app = Flask(__name__)

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
        return redirect("/protected")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users.insert_one(
            {
                "email": request.form.get("email"),
                "password": request.form.get("password"),
                "image": request.form.get("photo"),
                "face_id": [],
                "date": datetime.utcnow(),
            }
        )
        return redirect("/protected")

    return render_template("register.html")


@app.route("/protected")
def protected():
    return render_template("protected.html")


if __name__ == "__main__":
    app.run()
