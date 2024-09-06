from flask import request, jsonify
from . import routes
from utils.fingerprint_utils import enroll_fingerprint

@routes.route('/enroll-fingerprint', methods=['POST'])
def enroll_fingerprint_route():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    
    response, status_code = enroll_fingerprint(full_name, email, password)
    
    return jsonify(response), status_code
