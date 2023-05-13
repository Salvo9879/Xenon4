""" Paths is used to control all the directories & files creation & removal. It also provides the rest of the program with paths to essential directories for easy modifications if required in later 
version releases. It takes charge of all JSON file parsing & also converts relative paths to absolute. """



# Import internal packages
from source.exceptions import InvalidFileExtension

# Import standard packages
import os
import shutil
import json



class Paths():
    ABS_PATH = os.path.abspath('.') # The absolute path to the programs base directory.

    # Instance
    INSTANCE_ABS_PATH = os.path.join(ABS_PATH, 'instance') # The absolute path to the programs instance directory.
    SETTINGS_ABS_PATH = os.path.join(INSTANCE_ABS_PATH, 'system.ini')

def join_paths(*paths: str) -> str:
        """ Returns an absolute path joined to a give path. 

        Example: 
        ```python
        paths = Paths()
        paths.join_paths('directory1', 'directory2', 'directory3')
        >>> '<absolute_path>/directory1/directory2/directory3'
        ```
        
        Params:
            - paths: (str) - Allows the program to pass multiple paths to be joined. """
        
        # Returns the joined path of the base programs absolute path & any given path as a parameter.
        return os.path.join(Paths.ABS_PATH, *paths)



def create_file(path: str) -> None:
    """ Creates a file with at a given path.
        
    Params:
        - path (str) - A path to where the file will be made. """

    # Creates the file using `open`. Nothing is written.
    with open(path, 'x') as _:
        pass

def delete_file(path: str) -> None:
    """ Deletes a file at a given path.
        
    Params:
        - path (str) - A path to where the targeted file is located. """

    # Removes the file.
    os.remove(path)

def read_file_json(path: str) -> any:
    """ Returns the content of a file at a given path & parses it to JSON. 
    
    Params: 
        - path (str) - A path to where the targeted file is located. The extension of the targeted file must be `.json`. """

    # Checks if the path ends with `.json`. If so, raises an exception.
    if not path.endswith('.json'):
        raise InvalidFileExtension('Extension must be \'.json\'.')

    # Opens the given file for reading & json parses the internal content.
    with open(path, 'r') as f:
        data = json.load(f)

    # Returns the internal content to the caller.
    return data

def write_file_json(path: str, content: any) -> None:
    """ Attempts to parse content as JSON & writes it to a file at a given path. 
    If the file does not exist, then it will be created.
    
    Params:
        - path (str) - A path to where the targeted file is located. The extension of the targeted file must be `.json`. """
    
    # Checks if the path ends with `.json`. If so, raises an exception.
    if not path.endswith('.json'):
        raise InvalidFileExtension('Extension must be \'.json\'.')
    
    # Opens the given file for writing & dumps the json parsed content.
    with open(path, 'w') as f:
        json.dump(content, f)

def rename_file(path: str, new_name: str) -> None:
    """ Renames a file at a given path.
        
    Params:
        - path (str) - A path to where the targeted file is located. The extension of the targeted file must be `.json`.
        - new_name (str) - The name to replace the old name of the file. """
    
    # Checks if the path ends with `.json`. If so, raises an exception.
    if not path.endswith('.json'):
        raise InvalidFileExtension('Extension must be \'.json\'.')

    # Renames the file.
    os.rename(path, new_name)

def file_exists(path: str) -> bool:
    """ Returns a bool based on whether a file at a given path exists.
        
    Params:
        - path (str) - A path to where the targeted file is located. """

    # Checks if the file exists.
    return os.path.exists(path)



def create_directory(path: str) -> None:
    """ Creates a named directory at a given path.
        
    Params:
        - path (str) - A path to where the directory will be made. """

    # Creates the new directory.
    os.mkdir(path)

def delete_directory(path: str, name: str) -> None:
    """ Deletes an empty directory at the given path.
    Use this function for all cases except for removing packages. Else use `Directories.delete_directories_full()`. 
    NOTE: The directory must be empty. To delete a directory with content, use `Directories.delete_directory_full()`.
        
    Params:
        - path (str) - The path in which the targeted directory is located. """

    # Deletes the empty directory.
    os.rmdir(path)

def delete_directory_full(path: str) -> None:
    """ Deletes a directory at a given path which may have child content.
    This should only be used to remove packages. Else use `Directories.delete_directories()`.
        
    Params:
        - path (str) - The path of which the targeted directory is located. """

    # Deletes the directory & all its internal content.
    shutil.rmtree(path)

def delete_directory_content(path: str) -> None:
    """ Deletes all the content in a directory at a given path. Will not delete the directory just the content inside.
    NOTE: All content will be deleted including those in subdirectories. 
    
    Params:
        - path (str) - The path of which the targeted directory is located. """
    
    # Gets all the directories & files in the given directory.
    content_found = find_content(path)

    # Iterates though the content & deletes all the sub-content found.
    for content in content_found:
        content_complete_path = join_paths(path, content)
        shutil.rmtree(content_complete_path)

def rename_directory(path: str, new_name: str) -> None:
    """ Renames a directory at a given path. It renames it to parameter `new_name`.
        
    params:
        - path (str) - The path of which the targeted directory is located.
        - new_name (str) - The name to replace the old name of the directory. """

    # Renames the directory.
    os.rename(path, new_name)

def find_content(path: str) -> list[str]:
    """ Returns a list of all the content found in a directory at a given path. 
    
    params:
        - path (str) - The path in which the targeted directory is located. """

    # Returns a list of all the directories & files the directory.
    return os.listdir(path)

def directory_exists(path: str) -> bool:
    """ Returns a bool based on whether a directory at a given path exists..
        
    Params:
        - path (str) - The path in which the targeted directory is located. """

    # Checks if the directory exists.
    return os.path.exists(path)