import requests
import random


class Wordbook(object):
    """Class to create words used in Hangman game"""

    def __init__(self):
        """creates Wordbook object"""
        self.book = None
        self.indexes = set()


    def create_wordbook(self):
        """accesses API to retrieve list of words"""

        payload = {'difficulty': None,
                    'minLength': None,
                    'maxLength': None,
                    'start': 162410,
                    'count': None}
        r = requests.get('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words', params=payload)

        self.book = r.text.split()

    def select_word(self):
        """ Selects a psudo-random word from the book
            Returns a list object of word. ie. 'ant' = ['a','n','t']"""

        rand_num = random.randint(0, len(self.book)-1)

        while rand_num in self.indexes:
            rand_num = random.randint(0, len(self.book)-1)

        self.indexes.add(rand_num)
        secret_word = list(self.book[rand_num])

        return secret_word




