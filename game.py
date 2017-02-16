import wordbook
import utilities as util

class Hangman (object):
    """class for the hangman game"""

    def __init__(self):
        self.dictionary = wordbook.WordBook()
        self.secret_word = None
        self.guess = None
        self.missed_letters = None
        self.guesses = set()

    