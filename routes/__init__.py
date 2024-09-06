from flask import Blueprint

# Initialize the Blueprint
routes = Blueprint('routes', __name__)

# Import the different route modules
from . import register
from . import enroll_fingerprint
    