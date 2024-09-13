from flask import Blueprint, request, jsonify, render_template, current_app
from datetime import datetime
from . import routes
from models.users import User
from models.logs import LoginLog
import jwt
from flask import render_template

@routes.route('/logout')
def home():
    return render_template('logout.html')

@routes.route('/logging_out', methods=['POST'])
def logout():
    try:
        # Get the user's IP or session info here if needed, or fetch from the database directly.
        # Assuming the user is somehow authenticated and we have their user_id in the session.
        
        # Find the user by session or another identifying method (e.g., logged-in session)
        user = User.objects(active=True).first()  # This is a placeholder, adjust based on your actual logic

        if not user:
            return jsonify({'error': 'No active user found'}), 404

        # Fetch the latest login log
        latest_login_log = LoginLog.objects(user=user).order_by('-login_time').first()

        if not latest_login_log:
            return jsonify({'error': 'No active login session found for this user'}), 404

        # Check if the session is already logged out
        if latest_login_log.logout_time:
            return jsonify({'error': 'User is already logged out from this session'}), 400

        # Check if the user logged in on the same day
        if latest_login_log.login_time.date() != datetime.utcnow().date():
            return jsonify({'error': 'User did not log in today'}), 400

        # Proceed to log out
        user.update(set__active=False)
        latest_login_log.update(set__logout_time=datetime.utcnow())

        return jsonify({'message': 'Logout successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
