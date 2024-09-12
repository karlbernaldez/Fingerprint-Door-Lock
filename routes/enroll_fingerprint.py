from flask import request, jsonify
from . import routes
from utils.fingerprint_utils import start_fingerprint_enrollment, complete_fingerprint_enrollment

@routes.route('/start-fingerprint-enrollment', methods=['POST'])
def start_fingerprint_enrollment_route():

    #Sample Payload
    # {
    # "full_name": "John Doe",
    # "email": "john.doe@example.com",
    # "password": "securepassword123"
    # }

    full_name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Initialize fingerprint enrollment
    response, status_code = start_fingerprint_enrollment(full_name, email, password)

    return jsonify(response), status_code

@routes.route('/complete-fingerprint-enrollment', methods=['POST'])
def complete_fingerprint_enrollment_route():
    # Complete the fingerprint enrollment
    response, status_code = complete_fingerprint_enrollment()

    return jsonify(response), status_code
