import os
from flask import Flask
from flask_mongoengine import MongoEngine
from routes import routes  # Import the routes Blueprint

app = Flask(__name__)
app.secret_key = "8c46f38b7d4f5a8e83b1e93a6e26d6c5bb149b1ac8dcd5a64b9d7a2e7b3e23c1"
app.config['SECRET_KEY'] = '8c46f38b7d4f5a8e83b1e93a6e26d6c5bb149b1ac8dcd5a64b9d7a2e7b3e23c1'


# # Initialize MongoDB
# connection_string = os.getenv("MONGODB_URI", "mongodb+srv://fingerprint_db:admin1234@thesis.ro0a8.mongodb.net/?retryWrites=true&w=majority&appName=Thesis")
# client = MongoClient(connection_string)
# db = client.get_database("fingerprints")

# Configure MongoEngine
app.config['MONGODB_SETTINGS'] = {
    'db': 'fingerprints',
    'host':'mongodb+srv://fingerprint_db:admin1234@thesis.ro0a8.mongodb.net/?retryWrites=true&w=majority&appName=Thesis',
    'alias': 'default',
    'connect': False,
    'tls': True,  # Enable TLS
    'tlsAllowInvalidCertificates': False
}

# Initialize MongoEngine with the app
db = MongoEngine()
db.init_app(app)

# try:
#     db.create_collection("fingerprints", validator=user_validation_schema)
# except CollectionInvalid as e:
#     print(e)

# users = db.get_collection("fingerprints")
# users.create_index("email", unique=True)

# Register the Blueprint
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
