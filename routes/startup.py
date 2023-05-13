""" A route script which contains all the routing code used for the servers start up sequence. Generally anything relating to setting up the server for the first time. This may include setting up the
admin account, setting system settings, security fail safes, networking & internet configurations, corruption fallbacks etc. """

# Import external packages
from flask import Blueprint, render_template

# Blueprint registration
startup_r = Blueprint('startup', __name__, url_prefix='/startup')

# Routes
@startup_r.route('/')
def index():
    return render_template('index.html')