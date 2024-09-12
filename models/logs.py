from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

# Define the LoginLog model
class LoginLog(db.Document):
    user = db.ReferenceField('User', required=True)  # Reference to the User who logged in
    user_id = db.StringField(required=True)  # User ID of the logged-in user
    full_name = db.StringField(required=True)
    login_method = db.StringField(choices=["FINGERPRINT", "EMAIL&PASSWORD"])
    login_time = db.DateTimeField(default=datetime.datetime.utcnow)
    logout_time = db.DateTimeField()
    session_id = db.StringField(required=True, unique=True)

    def get_full_name(self):
        """Retrieve full name from the referenced User."""
        if self.user:
            return self.user.full_name
        return "Unknown User"