import wordbook
import utilities as util

class Hangman (object):
    """class for the hangman game"""

    def __init__(self):
        self.dictionary = wordbook.Wordbook()
        self.secret_word = None
        self.guess = None
        self.missed_letters = []
        self.guesses = set()
        self.num_guesses = 6

    def set_dictionary(self):
        self.dictionary.create_wordbook()

    def set_secret_word(self):
        self.secret_word = self.dictionary.select_word()

    def set_guess(self):
        self.guess = ['_'] * len(self.secret_word)


    def game_over(self):

        if self.num_guesses > 0 and self.secret_word != self.guess:
            return False

        return True

    def find_letter_in_word(self, letter):
        """ Looks for letter in word
            Returns [] of matching indexes, Empty [] = Not found """

        index = []

        for i, char in enumerate(self.secret_word):
            if char == letter:
                index.append(i)

        return index 

    def update_guess(self, indexes, letter):
        """ Replaces '_' with letter at indexes of guess 
            Returns updated guess """

        for i in indexes:
            self.guess[i] = letter


    def update_num_guesses(self):
        self.num_guesses -= 1

    def update_missed(self, letter):
        self.missed_letters.append(letter)



