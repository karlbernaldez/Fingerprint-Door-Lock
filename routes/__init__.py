from flask import Blueprint

# Initialize the Blueprint
routes = Blueprint('routes', __name__)

print("Importing register module")
from . import register

print("Importing enroll_fingerprint module")
from . import enroll_fingerprint
