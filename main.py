import os
from flask import Flask
from pymongo import MongoClient
from routes import routes  # Import the routes Blueprint
from utils.validation_schema import user_validation_schema
from pymongo.errors import CollectionInvalid, DuplicateKeyError

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize MongoDB
connection_string = os.getenv("MONGODB_URI", "mongodb+srv://fingerprint_db:admin1234@thesis.ro0a8.mongodb.net/?retryWrites=true&w=majority&appName=Thesis")
client = MongoClient(connection_string)
db = client.get_database("fingerprints")

try:
    db.create_collection("fingerprints", validator=user_validation_schema)
except CollectionInvalid as e:
    print(e)

users = db.get_collection("fingerprints")
users.create_index("email", unique=True)

# Register the Blueprint
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
