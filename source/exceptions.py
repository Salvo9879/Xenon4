""" These are custom exceptions which could rise in the program. Each will have different cases in what the system does. """

# Paths
class InvalidFileExtension(Exception):
    """ Raised when the `source.paths.Files.create_file()` is given an invalid file extension. This is usually due to the extension not starting with a `.`. """
    pass