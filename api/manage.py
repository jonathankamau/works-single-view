import os

import sys
sys.path.append(os.getcwd())

from flask_script import Manager
from api.app import create_app
from api.utils.models import db

movie_app = create_app(environment=os.environ.get('APP_SETTINGS'))
manager = Manager(movie_app)

if __name__ == "__main__":
    manager.run()