""" This is the centralized server configuration file. Everything relating to the server is built out from here. Here we handle the server configuration, system routing, applications, application 
routing, databases, authentication, context processing etc. """

# Import internal packages
from source.config import SettingsManager

# Import external packages
from flask import Flask

# Variables
server = Flask(__name__)
settings_manager = SettingsManager()