from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime

class LoginLog(Document):
    user = ReferenceField('User', required=True)  # Reference to the User who logged in
    full_name = StringField(required=True)
    login_time = DateTimeField(default=datetime.datetime.utcnow)
    logout_time = DateTimeField()

    def get_full_name(self):
        """Retrieve full name from the referenced User."""
        if self.user:
            return self.user.full_name
        return "Unknown User"
 