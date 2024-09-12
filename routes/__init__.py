from flask import Blueprint

# Initialize the Blueprint
routes = Blueprint('routes', __name__)

from . import register
from . import enroll_fingerprint
from . import fetch
from . import login
from . import logout
