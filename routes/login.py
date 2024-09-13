from flask import Blueprint, jsonify, request, current_app, render_template
from models.users import User
from models.logs import LoginLog
from werkzeug.security import check_password_hash
from . import routes
from datetime import datetime, timedelta
import jwt


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
    data = request.get_json()
    template_position = data.get('template_position')
    
    if not template_position:
        return jsonify({'error': 'Template position and fingerprint ID are required'}), 400

    user = User.objects(template_position=template_position).first()
    if user:
        # Update user fields
        user.active = True
        user.last_login = datetime.datetime.utcnow()
        user.save()
        
        # Log the login event
        login_log = LoginLog(
            user=user,
            full_name=user.full_name,
            login_method="FINGERPRINT",
            session_id=generate_session_id()  # Implement this function to generate unique session IDs
        )
        login_log.save()
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user.user_id,
            'full_name': user.full_name,
            'role': user.role
        })
    else:
        return jsonify({'error': 'Invalid fingerprint or template position'}), 401

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
         # Log the login event
        login_log = LoginLog(
            user=user,
            user_id=user.user_id,
            full_name=user.full_name,
            login_method="EMAIL&PASSWORD",
            session_id=generate_session_id()  # Implement this function to generate unique session IDs
        )
        login_log.save()
        
        return jsonify({
            'message': 'Login successful',
            "user": user,
            "user_id": user.user_id,
            "full_name": user.full_name,
            "login_method": "EMAIL&PASSWORD",
            "session_id": generate_session_id(),
            'token': token,
        })
    else:
        return jsonify({'error': 'Invalid email or password'}), 401