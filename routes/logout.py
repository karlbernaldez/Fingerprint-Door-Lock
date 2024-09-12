from flask import Blueprint, request, jsonify
from datetime import datetime
from . import routes
from models.users import User
from models.logs import LoginLog
import jwt

@routes.route('/logout', methods=['POST'])
def logout():
    # Extract the token from the Authorization header
    token = request.headers.get('Authorization')
    if token:
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400
            
            # Fetch the user
            user = User.objects(user_id=user_id).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Fetch the latest LoginLog entry for this user by sorting by login_time
            latest_login_log = LoginLog.objects(user=user).order_by('-login_time').first()
            if not latest_login_log:
                return jsonify({'error': 'No active login session found for this user'}), 404
            
            # Check if the session is already logged out
            if latest_login_log.logout_time:
                return jsonify({'error': 'User is already logged out from this session'}), 400
            
            # Update the User document to set active to False
            user.update(set__active=False)
            
            # Update the LoginLog document to set logout_time to now
            latest_login_log.update(set__logout_time=datetime.utcnow())
            
            return jsonify({'message': 'Logout successful'}), 200
        
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    else:
        return jsonify({'error': 'Authorization token is missing'}), 401
