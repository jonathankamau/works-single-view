import configparser
from flask import Flask, jsonify
from flask_cors import CORS

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api
from api.endpoints.get_music_works import RetrieveMusicWork, UploadMusicWorks
from api.utils.models import db

import api.flask_configs as configs



def create_app(environment):
    """Factory Method that creates an instance of the app with the given config."""
    
    app = Flask(__name__)
    app.config.from_object(configs.Local)
    db.init_app(app)

    api = Api(
        app=app,
        default='Api',
        title='Works Single View',
        version='1.0.0',
        description="Works Single View API"
        )
    # enable cross origin resource sharing
    CORS(app)

    api.add_resource(RetrieveMusicWork, "/api/v1/<iswc>",
                     endpoint="single_music_work")
    api.add_resource(UploadMusicWorks, "/upload",
                     endpoint="music_work_upload")

    # handle default 404 exceptions
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(
            error='Not found',
            message='The requested URL was not found on the server.'))
        response.status_code = 404
        return response

    # handle default 500 exceptions
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(
            error='Internal server error',
            message="The server encountered an internal error."))
        response.status_code = 500
        return response

    return app
