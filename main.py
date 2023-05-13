""" This is the script which should be run. This configures, loads & deploys the system functionality. """

# Import internal packages
from source.server import server, settings_manager

if __name__ == '__main__':
    server.run(
        host=settings_manager.server_host,
        port=settings_manager.server_port,
        debug=settings_manager.server_debug
    )
