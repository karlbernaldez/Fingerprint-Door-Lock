from mongoengine import Document, StringField, BinaryField, IntField, DateTimeField, EmailField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from bson.binary import Binary
import datetime
import pickle
import jwt
import os

# Secret key for JWT token
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

class User(Document):
    full_name = StringField(required=True, max_length=200)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)  # Hashed password
    fingerprint_id = BinaryField(required=True)  # Storing the binary representation of the fingerprint template
    template_position = IntField(required=True)  # Position in the fingerprint sensor
    date = DateTimeField(default=datetime.datetime.utcnow)
    active = BooleanField(default=False)  # Tracks if the user is currently logged in
    token = StringField()  # JWT token for login sessions
    last_login = DateTimeField()  # Tracks the last login time

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_fingerprint(self, fingerprint):
        self.fingerprint_id = Binary(pickle.dumps(fingerprint))

    def generate_token(self):
        self.token = jwt.encode(
            {"email": self.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256"
        ).decode('utf-8')
        return self.token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["email"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def update_last_login(self):
        self.last_login = datetime.datetime.utcnow()
        self.save()

    def set_active(self, status):
        self.active = status
        self.save()
    