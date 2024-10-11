from flask_mongoengine import MongoEngine
import datetime
import random
import string
import jwt, os
from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

# Secret key for JWT token
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

class User(db.Document):
    user_id = db.StringField(required=True, unique=True)
    full_name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    fingerprint_id = db.BinaryField()
    template_position = db.IntField()
    date = db.DateTimeField(default=datetime.datetime.utcnow)
    active = db.BooleanField(default=False)
    verified = db.BooleanField(default=False)
    token = db.StringField()
    last_login = db.DateTimeField()
    role = db.StringField(choices=["ADMIN", "CLIENT"], default="CLIENT")

    meta = {
        'collection': 'fingerprints'}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_fingerprint(self, fingerprint_data):
        self.fingerprint_id = fingerprint_data

    def generate_token(self):
        token = jwt.encode(
            {"email": self.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256"
        )
        self.token = token
        self.save()  # Save the token to the database
        return token

    def verify_token(self, token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return data
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}

    def update_last_login(self):
        self.last_login = datetime.datetime.utcnow()
        self.save()

    def set_active(self, status):
        self.active = status
        self.save()

    @staticmethod
    def generate_user_id():
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=4))
        return letters + numbers
