from flask import Blueprint, jsonify
from models.users import User
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

