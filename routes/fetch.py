from flask import Blueprint, jsonify
from models.users import User
from models.logs import LoginLog
from . import routes
import base64

@routes.route('/user/<full_name>', methods=['GET'])
def get_user_by_name(full_name):
    user = User.objects(full_name=full_name).first()
    if user:
        return jsonify({
            'user_id': user.user_id,
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'fingerprint_id': base64.b64encode(user.fingerprint_id).decode('utf-8') if user.fingerprint_id else None,
            'template_position': user.template_position,
            'date': user.date.isoformat(),
            'active': user.active,
            'token': user.token,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'role': user.role
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@routes.route('/users', methods=['GET'])
def get_all_users():
    users = User.objects()
    user_list = []
    for user in users:
        user_list.append({
            'user_id': user.user_id,
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'fingerprint_id': base64.b64encode(user.fingerprint_id).decode('utf-8') if user.fingerprint_id else None,
            'template_position': user.template_position,
            'date': user.date.isoformat(),
            'active': user.active,
            'token': user.token,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'role': user.role
        })
    return jsonify(user_list)

@routes.route('/user/template_position/<int:template_position>', methods=['GET'])
def get_user_by_template_position(template_position):
    user = User.objects(template_position=template_position).first()
    if user:
        return jsonify({
            'user_id': user.user_id,
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'fingerprint_id': base64.b64encode(user.fingerprint_id).decode('utf-8') if user.fingerprint_id else None,
            'template_position': user.template_position,
            'date': user.date.isoformat(),
            'active': user.active,
            'token': user.token,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'role': user.role
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@routes.route('/user/id/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.objects(user_id=user_id).first()
    if user:
        return jsonify({
            'user_id': user.user_id,
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'fingerprint_id': base64.b64encode(user.fingerprint_id).decode('utf-8') if user.fingerprint_id else None,
            'template_position': user.template_position,
            'date': user.date.isoformat(),
            'active': user.active,
            'token': user.token,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'role': user.role
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@routes.route('/logs', methods=['GET'])
def get_all_login_logs():
    logs = LoginLog.objects()
    log_list = []
    for log in logs:
        log_list.append({
            'user_id': log.user.user_id if log.user else None,
            'full_name': log.full_name,
            'login_method': log.login_method,
            'login_time': log.login_time.isoformat() if log.login_time else None,
            'logout_time': log.logout_time.isoformat() if log.logout_time else None,
            'session_id': log.session_id
        })
    return jsonify(log_list)

@routes.route('/user/<user_id>/login_logs', methods=['GET'])
def get_login_logs_for_user(user_id):
    user = User.objects(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    logs = LoginLog.objects(user=user)
    log_list = []
    for log in logs:
        log_list.append({
            'full_name': log.full_name,
            'login_method': log.login_method,
            'login_time': log.login_time.isoformat() if log.login_time else None,
            'logout_time': log.logout_time.isoformat() if log.logout_time else None,
            'session_id': log.session_id
        })
    return jsonify(log_list)