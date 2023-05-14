""" This is the centralized server configuration file. Everything relating to the server is built out from here. Here we handle the server configuration, system routing, applications, application 
routing, databases, authentication, context processing etc. """

# Import internal packages
from source.config import SettingsManager
from source.databases import DatabasesManager
from source.databases import Users
from source.paths import Paths
from routes import base_r

# Import external packages
from flask import Flask
from flask_login import LoginManager

# Variables
server = Flask(__name__)
settings_manager = SettingsManager()
databases_manager = DatabasesManager()
login_manager = LoginManager()

# Server configuration
server.template_folder = Paths.TEMPLATES_ABS_PATH
server.static_folder = Paths.STATIC_ABS_PATH

# Initialization
login_manager.init_app(server)

# Blueprint registration
server.register_blueprint(base_r)

# Login user callback
@login_manager.user_loader
def load_user(user_id):
    return databases_manager.session.query(Users).filter_by(id=user_id).first()