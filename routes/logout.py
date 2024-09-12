from flask import Blueprint, request, jsonify
from datetime import datetime
from . import routes
from models.users import User
from models.logs import LoginLog

@routes.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    
    if not user_id or not session_id:
        return jsonify({'error': 'User ID and session ID are required'}), 400
    
    # Update the User document to set active to False
    user = User.objects(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.update(set__active=False)
    
    # Update the LoginLog document to set logout_time
    login_log = LoginLog.objects(session_id=session_id).first()
    if not login_log:
        return jsonify({'error': 'Session ID not found'}), 404
    
    login_log.update(set__logout_time=datetime.utcnow())
    
    return jsonify({'message': 'Logout successful'}), 200
