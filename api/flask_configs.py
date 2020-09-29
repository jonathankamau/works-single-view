"""App environment configurations."""
import configparser
from scripts.database_connection import DatabaseConnection

conn = DatabaseConnection()

class Local():
    """Model local enviroment config object."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{conn.db_username}:{conn.db_password}@localhost:5432/{conn.db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ALLOWED_EXTENSION = {'csv'}
    UPLOAD_FOLDER = 'data'
