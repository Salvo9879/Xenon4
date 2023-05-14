""" Holds all the tables for Xenons databases. All system tables are stored in the `/instance/xenon.db` database file. Our database utilizes a SQLAlchemy database structure & a sqlite engine. 
NOTE: Only the system tables are modeled in this file. All application database must be stored in the applications base directory. """


# Import internal packages
from source.paths import Paths
from source.exceptions import ProfileTypeStillActive

import source.helpers as helpers

# Import external packages
from sqlalchemy import create_engine, Column
from sqlalchemy.types import String, Integer, DateTime, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

# Variables
base = declarative_base()

class DatabasesManager():
    """ In charge of the all the tables used for system functionality. Upon initialization (this should be done in the `/source/server.py`), the engine, session maker & all tables are created & 
    formatted in the `/instance/xenon.db` database file.
     
    To query any database, you must use `session.query(<TABLE>)`. Example: To query from the `Users` table, you write the following:
    ```python
    from source.databases import DatabasesManager, Users

    databases_manager = DatabasesManager()

    found_user = databases_manager.session.query(Users).filter_by(id=1).first() # Returns the first row in which `id=1`.
    found_user = databases_manager.session.query(Users).filter_by(profile_type=1) # Returns a list of all rows where `profile_type=1`.
    ``` """
    def __init__(self) -> None:
        # Create the database engine.
        db_engine = create_engine(Paths.DB_ABS_PATH, echo=False)

        # Create all the tables & the `/instance/xenon.db` file.
        base.metadata.create_all(bind=db_engine)

        # Initialize the session maker. 
        _session = sessionmaker(bind=db_engine)
        self.session = _session()

    def add_row(self, instance: object) -> None:
        """ Adds an instance to the databases table. To do this create an instance of the object table you would like to add to. Then format the property values & then pass that instance to this 
        function. Example:
        ```python
        from source.databases import DatabasesManager, ProfileTypes

        databases_manager = DatabasesManager()

        profile_type = ProfileTypes()
        profile_type.name = 'Admin'
        profile_type.description = 'Gives the user access to restricted pages of the web application.'

        databases_manager.add_row(profile_type)
        ``` 
        
        Params:
            - instance (object) - The instance of the table object that should be added. """

        # Add the row to the session.
        self.session.add(instance)

        # Commits the session to the database.
        self.session.commit()

    def delete_row(self, instance: object) -> None:
        """ Deletes an instance from the databases table. To do this query the database to get the instance of the row you would like to delete. Pass the instance to this function. Example:
        ```python
        from source.databases import DatabasesManager, Users

        databases_manager = DatabasesManager()
         
        user = databases_manager.session.query(Users).filter_by(email='johndoe@test.com').first()
        databases_manager.delete_row(user) 
        ```
        
        NOTE: There are exceptions about if rows are deleted. Some may fail & raise relevant exceptions. The exceptions are as follows:
            - If the row attempting to delete is under the `ProfileTypes` table, then the deletion process may fail if that profile type is still assigned to 1 or more users.
            
        Params: 
            - instance (object) - The instance of the table object that should be deleted. """

        # Checks if the instance is of `ProfileTypes`. If so it gets a list of all users assigned to that profile type.
        if isinstance(instance, ProfileTypes):
            users_with_profile_type = self.session.query(Users).filter_by(ProfileTypes=instance.id)

            # If there are used discovered to be assigned under that profile type, then raise an exception.
            if users_with_profile_type:
                raise ProfileTypeStillActive(instance.name)

        # Deletes the row from the session.
        self.session.delete(instance)

        # Commits the session to the database.
        self.session.commit()

class ProfileTypes(base):
    """ Holds information about profile types. So in Xenon, the consumers can create different profile types which change what privileges & permissions that user has. Examples of profile types can be
    'Admin', 'Adult', 'Child', 'Guest' etc. The user can create these profile types in the settings application & then assign them to the users. To add a new privilege/permission, you must add a 
    column which generally should be type bool, however there are exceptions.
    NOTE: You will not be able to delete a profile type until no user is assigned that profile type. 
    
    Properties: 
        - id (int) - This is the rows primary key.
        - name (str) - This is the name of the profile type. May also be called a profile title. 
        - description (str) - A general description to describe what the profile type does. """
    
    # Create the table name.
    __tablename__ = 'profile_types'

    # Initialize the table columns. 
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    description = Column('description', String)


class Users(base):
    """ The users database table is used to store information about the users. Each person in the household should have a profile. These profiles are stored in this table. The main use of these 
    profiles is so that different users have access to different data stored (mainly in apps). For example you don't want your exercise information from a tracker visible to the whole household - so
    all the data is stored in databases & protected under a authentication policy. Another reason to create profiles is to limit what different profile types can access on the Xenon server. Like 
    let's say a household has children, we would give them a profile type in which limits them from accessing Xenons admin panel.
     
    Properties:
        - id (int) - This is the rows primary key. 
        - forename () - This is the users forename. 
        - surname () - This is the users surname. 
        - email () - This needs to be a valid, unique & active email address. 
        - username () - This needs to be a unique username. 
        - date_of_birth () - The ISO 8601 date that the user was born. 
        - datetime_of_creation () - This is the ISO 8601 datetime of when the row was created. 
        - hashed_password () - This is the hashed version of the users password. 
        - profile_type () - This is the primary key (id) of the profile type the user is assigned to. """

    # Create the table name.
    __tablename__ = 'users'

    # Initialize the table columns.
    id = Column('id', Integer, primary_key=True)

    forename = Column('forename', String)
    surname = Column('surname', String)

    email = Column('email', String, unique=True)
    username = Column('username', String, unique=True)

    date_of_birth = Column('date_of_birth', Date)
    datetime_of_creation = Column('datetime_of_creation', DateTime, default=helpers.convert_to_iso(helpers.get_current_datetime()))

    hashed_password = Column('hashed_password', String)

    profile_type = Column('profile_type', Integer)

    def set_profile_type(self, profile_type_id: Column[int]) -> None:
        """ Sets the property `profile_type` to the profile type row id.
         
        Params:
            - profile_type_id (Column[int]) - The primary key (id) of the row in the `ProfilesTable` table that the user should be assigned to. """
        
        # Sets the `profile_type` property to parameter `profile_type_id`.
        self.profile_type = profile_type_id

    @property
    def password(self) -> AttributeError:
        """ This attribute is not stored in the database. """

        # Raises an exception.
        raise AttributeError('Property \'password\' is not a readable attribute.')
    
    @password.setter
    def password(self, password: str) -> None:
        """ Sets the `hashed_password` property to a hashed version of the given clear text password.
         
        Params:
            - password (str) - The clear text password which will be hashed & stored. """
        
        # Sets the property `hashed_password` to a hashed version of parameter `password`.
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """ Returns a bool based on whether a given clear text password matches a stored hashed version.
         
        Params:
            - Password (str) - The clear text password you would like to check. """
        
        # Returns the value from the `werkzeug.security.check_password_hash` function.
        return check_password_hash(self.hashed_password, password)