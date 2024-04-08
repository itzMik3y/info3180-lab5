# Add any model classes for Flask-SQLAlchemy here
from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)  # Stores the filename of the poster
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Movie {self.title}>'
