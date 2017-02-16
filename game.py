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
        self.num_of_guesses = 6

    def set_dictionary(self):
        self.dictionary.create_wordbook()

    def get_secret_word(self):
        self.secret_word = self.dictionary.select_word()

    def set_guess(self):
        self.guess = ['_'] * len(self.secret_word)

    
