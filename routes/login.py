from flask import Blueprint, jsonify, request, current_app, render_template
from models.users import User
from models.logs import LoginLog
from werkzeug.security import check_password_hash
from . import routes
from datetime import datetime, timedelta
import jwt
from pyfingerprint.pyfingerprint import PyFingerprint
from time import sleep
from utils import fingerprint_utils
import pyttsx3
from utils import tts as Text2Speech
import pygame


# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Utility function to generate unique session IDs
def generate_session_id():
    import uuid
    return str(uuid.uuid4())

@routes.route('/login')
def login():
    return render_template('login.html')

# Route for login using fingerprint template position
@routes.route('/login/fingerprint', methods=['POST'])
def login_using_fingerprint():
    # Call the check_fingerprint function to check for a fingerprint match
    is_matched, template_position, accuracy_score = fingerprint_utils.check_fingerprint()

    if is_matched:
        user = User.objects(template_position=template_position).first()

        if user:
            welcome = Text2Speech.text_to_speech_file(f"Welcome to Mobile Legends {user.full_name}")
            pygame.mixer.music.load(welcome)
            pygame.mixer.music.play()
            # Update user fields
            user.active = True
            user.last_login = datetime.utcnow()
            user.save()

            # Log the login event
            login_log = LoginLog(
                user=user,
                full_name=user.full_name,
                login_method="FINGERPRINT",
                session_id=generate_session_id(),  # Implement this function to generate unique session IDs
                user_id=user.user_id  # Ensure this field is populated
            )
            login_log.save()
            print("LOGIN SAVED")
            return jsonify({
                'message': 'Login successful',
                'user_id': user.user_id,
                'full_name': user.full_name,
                'role': user.role,
                'matching_score': accuracy_score  # Include the matching score
            })
        else:
            return jsonify({'error': 'Invalid fingerprint or template position'}), 401
    else:
        return jsonify({
            'error': 'Fingerprint not matched',
            'matching_score': accuracy_score  # Include score even if no match
        }), 401

# Login route using email and password
@routes.route('/logging_in', methods=['POST'])
def login_using_email():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.objects(email=email).first()
    if user and check_password_hash(user.password, password):
         # Access the SECRET_KEY from Flask app's config
        SECRET_KEY = current_app.config['SECRET_KEY']
        # Generate a JWT token
        token = jwt.encode({
            'user_id': user.user_id,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiry (1 hour)
        }, SECRET_KEY, algorithm='HS256')


         # Update user fields
        user.active = True
        user.last_login = datetime.utcnow()
        user.save()
        user.token = token
        welcome = Text2Speech.text_to_speech_file(f"Welcome to Mobile Legends {user.full_name}")
        pygame.mixer.music.load(welcome)
        pygame.mixer.music.play()
         # Log the login event
        login_log = LoginLog(
            user=user,
            login_time=datetime.utcnow(),
            user_id=user.user_id,
            full_name=user.full_name,
            login_method="EMAIL&PASSWORD",
            session_id=generate_session_id()  # Implement this function to generate unique session IDs
        )
        login_log.save()
        
        return jsonify({
            'message': 'SUCCESS',
            "user": user,
            "user_id": user.user_id,
            "full_name": user.full_name,
            "login_method": "EMAIL&PASSWORD",
            "session_id": generate_session_id(),
            'token': token,
        })
    else:
        return jsonify({'error': 'Invalid email or password'}), 401