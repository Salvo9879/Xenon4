""" This is the centralized server configuration file. Everything relating to the server is built out from here. Here we handle the server configuration, system routing, applications, application 
routing, databases, authentication, context processing etc. """

# Import internal packages
from source.config import SettingsManager
from source.paths import Paths
from routes import base_r

# Import external packages
from flask import Flask

# Variables
server = Flask(__name__)
settings_manager = SettingsManager()

# Server configuration
server.template_folder = Paths.TEMPLATES_ABS_PATH
server.static_folder = Paths.STATIC_ABS_PATH

# Blueprint registration
server.register_blueprint(base_r)