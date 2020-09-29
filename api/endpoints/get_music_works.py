import csv
import os
import uuid
from datetime import datetime
from flask import (
    current_app, request, jsonify, 
    render_template, make_response, redirect)
from werkzeug.utils import secure_filename
from flask_restplus import Resource
from scripts.database_connection import DatabaseConnection


from utils.models import MusicWorks

database_conn = DatabaseConnection()

class RetrieveMusicWork(Resource):

    def export_csv(self, result):

        current_time = datetime.now()

        file_path = os.path.join(
            'output/', f'works_metadata-{datetime.timestamp(current_time)}.csv')
        
        

        with open(file_path, 'w') as new_file:
            file_action = csv.DictWriter(new_file, fieldnames=result.keys())
            file_action.writeheader()
            file_action.writerow(dict(result))


    def get(self, iswc):
        music_work = MusicWorks.query.filter_by(iswc=iswc).first()

        if music_work:

            result = {
                "iswc": music_work.iswc,
                "title": music_work.title,
                "contributors": music_work.contributors,
                "sources": music_work.sources
            }
        
            response = jsonify (
                message="The Music Work was retrieved successfully and is being exported as a csv",
                music_work=result

            )

            self.export_csv(result)

            response.status_code = 200
            
        else:
            response = jsonify (
                message="The Music Work could not be found!"
            )
        
            response.status_code = 400
    
        return response
    
    


class UploadMusicWorks(Resource):

    def get(self):

        headers = {'Content-Type': 'text/html'}

        return make_response(
            render_template('upload.html'),200,headers)

    def check_extension(self, filename):
        return '.' in filename and \
            filename.rsplit(
                '.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSION']



    def post(self):
        upload_file = request.files['upload']
        

        file_label = os.path.splitext(upload_file.filename)[0]
        file_extension = os.path.splitext(upload_file.filename)[1]

        new_file_name = file_label + str(uuid.uuid4()) + file_extension

        if upload_file and self.check_extension(upload_file.filename):

            secured_file_name = secure_filename(new_file_name)
            
            upload_file.save(
                os.path.join(current_app.config['UPLOAD_FOLDER'], secured_file_name))
            
            return redirect(request.url)
            
            database_conn.save_data()

        
        headers = {'Content-Type': 'text/html'}

        return make_response(
            render_template('upload.html'),200,headers)
