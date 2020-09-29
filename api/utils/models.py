from flask_sqlalchemy import SQLAlchemy

db  = SQLAlchemy()

class MusicWorks(db.Model):
    __tablename__ = "music_works"

    iswc = db.Column(db.String, unique=True, primary_key=True)
    title = db.Column(db.String)
    contributors = db.Column(db.String)
    sources = db.Column(db.String)