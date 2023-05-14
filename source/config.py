""" This is where all the configuration of the system occurs. All system settings are kept in a config file in the `instance` directory. (`/instance/settings.ini`). If the file does not exist, the 
settings manager will enter into a setup sequence, which automatically enters default settings for the system. This may block some features but can be modified in the servers dashboard. COMING SOON! """

# Import internal packages
from source.paths import Paths
from source.paths import directory_exists, create_directory
from source.paths import file_exists, create_file

# Import standard packages
import configparser

# Variables
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5000
DEFAULT_DEBUG = True #! Change to False on release

class SettingsManager():
    """ Handles all the system settings for Xenon. All configurable information is run strictly through this object. It will store all information in the `/instance/settings.ini` file. If this file 
    does not exist, then the settings manager will automatically create it & format the file to default values.
    
    NOTE: The manager auto creating the settings file may block several certain features; this can be modified in the servers dashboard. COMING SOON! """

    def __init__(self) -> None:
        # Creates the `ConfigParser` instance.
        self.cp = configparser.ConfigParser()

        # Checks if the `/instance` directory exists, if not it is created.
        if not directory_exists(Paths.INSTANCE_ABS_PATH):
            create_directory(Paths.INSTANCE_ABS_PATH)

        # Checks if the `/instance/system.ini` file exists, it calls the format function.
        if not file_exists(Paths.SETTINGS_ABS_PATH):
            self.format()
        
        # Calls the `deploy_values()` function.
        self.deploy_values()

    def format(self) -> None:
        """ Creates & formats the settings config file to it's default values. """

        # Creates the `/instance/system.ini` file.
        create_file(Paths.SETTINGS_ABS_PATH)

        # Creates the `SERVER` section in the `system.ini` file.
        section_name = 'SERVER'
        self.cp.add_section(section_name)

        # Sets the host, port & debug mode.
        self.cp.set(section_name, 'host', str(DEFAULT_HOST))
        self.cp.set(section_name, 'port', str(DEFAULT_PORT))
        self.cp.set(section_name, 'debug', str(DEFAULT_DEBUG))

        # Writes to the `/instance/system.ini` file all the config parser data.
        with open(Paths.SETTINGS_ABS_PATH, 'w') as f:
            self.cp.write(f)

    def deploy_values(self) -> None:
        """ Deploys the values stored in the settings config file. These values can now be accessed as properties. """

        # Deploys the information stored under the `SERVER` section as instance properties.
        section_name = 'SERVER'
        self.cp.read(Paths.SETTINGS_ABS_PATH)
        self.server_host = self.cp.get(section_name, 'host')
        self.server_port = self.cp.getint(section_name, 'port')
        self.server_debug = self.cp.getboolean(section_name, 'debug')