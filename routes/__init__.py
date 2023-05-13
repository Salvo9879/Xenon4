""" This is where all the blueprints are stored together. All blueprints are children of the `base_r` blueprint. This is then registered to the `Flask` instance. """

# Import external packages
from flask import Blueprint

# Import blueprints
from routes.startup import startup_r

# Base blueprint declaration
base_r = Blueprint('base', __name__)

# Base blueprint registration
base_r.register_blueprint(startup_r)