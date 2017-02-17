"""Models for Hangman"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import random

db = SQLAlchemy()


###########
# Model definitions

class Wordbook(db.Model):
    """dictionary of words"""

    __tablename__ = 'wordbook'

    wordbook_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book = db.Column(db.Text, nullable=False)
    

    def __init__(self, book):
        """creates Wordbook object"""
        self.book = book
   

class Used_index(db.Model):
    """indexes used for accessing words from dictionary"""

    __tablename__ = "used_index"

    used_index_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    index_num = db.Column(db.Integer, nullable=False)

    wordbook_id = db.Column(db.Integer, db.ForeignKey('wordbook.wordbook_id'))

    # Relationships
    wordbook = db.relationship('Wordbook', backref='Used_index')
    


######################
# Helper functions

def generate_wordlist():
    """access API to retrieve list of words"""

    payload = {'difficulty': None,
                'minLength': None,
                'maxLength': None,
                'start': 162410,
                'count': None}
    r = requests.get('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words', params=payload)

    # self.book = r.text.split()
    wordlist = r.text
    return wordlist

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hangman'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
