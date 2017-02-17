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
    indexes = db.Column(db.Text, nullable=True)

    def __init__(self, book=None):
        """creates Wordbook object"""
        self.book = book
        # self.indexes = set()
        self.indexes = []


    def create_wordbook(self):
        """accesses API to retrieve list of words"""

        payload = {'difficulty': None,
                    'minLength': None,
                    'maxLength': None,
                    'start': 162410,
                    'count': None}
        r = requests.get('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words', params=payload)

        # self.book = r.text.split()
        self.book = r.text

    def select_word(self):
        """ Selects a psudo-random word from the book
            Returns a list object of word. ie. 'ant' = ['a','n','t']"""

        rand_num = random.randint(0, len(self.book)-1)

        while rand_num in self.indexes:
            rand_num = random.randint(0, len(self.book)-1)

        self.indexes.add(rand_num)
        secret_word = list(self.book[rand_num])

        return secret_word

######################
# Helper functions

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
