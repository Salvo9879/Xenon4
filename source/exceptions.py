""" These are custom exceptions which could rise in the program. Each will have different cases in what the system does. """

# Paths
class InvalidFileExtension(Exception):
    """ Raised when the `source.paths.Files.create_file()` is given an invalid file extension. This is usually due to the extension not starting with a `.`. """
    pass

class ProfileTypeStillActive(Exception):
    """ Raised when a consumer attempts to delete a profile type from the database, however the database manager has found at least one user that is still using that profile type. """
    pass