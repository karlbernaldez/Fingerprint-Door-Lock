"""Main start app file."""

import os
import pickle
from datetime import datetime

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
)
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError
from werkzeug.security import generate_password_hash

from camera_utils import (
    check_face,
    generate_frames,
    get_face_id,
    take_screenshot_from_camera,
)
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
    """Log the user in using face id."""
    if request.method == "POST":
        user = users.find_one({"email": request.form.get("email")})

        if user:
            result = check_face(pickle.loads(user["face_id"]))

            if result:
                session["user"] = user["email"]
                flash(f"Welcome, {user['email']}!")
                return redirect(url_for("protected"))
            else:
                flash("Face ID does not match.")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Add new user to DB. Save a screenshot."""
    if request.method == "POST":
        try:
            screenshot = take_screenshot_from_camera(request.form.get("email"))
            face_id = get_face_id(screenshot)

            if screenshot and face_id:
                user_data = {
                    "email": request.form.get("email"),
                    "password": generate_password_hash(request.form.get("password")),
                    "image": f"user_screenshots/{request.form.get('email')}",
                    "face_id": Binary(pickle.dumps(face_id, protocol=2), subtype=128),
                    "date": datetime.utcnow(),
                }
                add_user = users.insert_one(user_data)

                if add_user:
                    app.logger.error(f"add_user: {add_user}")
                    return redirect(url_for("protected"))

                flash("Error. Cannot save data to DB.")

            else:
                app.logger.error(f"screenshot: {screenshot}")
                app.logger.error(f"face_id: {face_id}")
                flash("Cannot get face encoding, retake picture.")

        except DuplicateKeyError:
            flash("The given email already exists.")

        except Exception as error:
            app.logger.error(f"An error occurred while registering a user: {error}")
            flash("An error occurred while registering. Please try again later.")

    return render_template("register.html")


@app.route("/protected")
def protected():
    return render_template("protected.html")


if __name__ == "__main__":
    app.run()
