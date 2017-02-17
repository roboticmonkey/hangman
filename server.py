""" Server File """

from jinja2 import StrictUndefined
from flask import Flask, render_template, session, request
from flask_debugtoolbar import DebugToolbarExtension
import random
# import hangman
import utilities as util
from model import connect_to_db, Wordbook, db, Used_index, generate_wordlist


app = Flask(__name__)

app.secret_key = "something-secret"

app.jinja_env.undifined = StrictUndefined

########
# Routes

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    
    num = 6
    session['num_left'] = num
    session['letters'] = []

    # Generate the wordlist via api
    words = generate_wordlist()
    
    # Create a wordbook object, add to db
    new_dic = Wordbook(book=words)
    db.session.add(new_dic)
    db.session.commit()

    # Save wordbook id in session var - for later use 
    session['id'] = new_dic.wordbook_id

    # Select a secret word from wordbook
    secret_word = select_word(new_dic)
    session['secret_word'] = secret_word

    # Generate a guess word based on secret word length
    guess_list = ['_'] * len(secret_word)

    # Save guess in session var
    session['guess'] = guess_list

    guess = convert_to_string(guess_list)

    return render_template('game.html', guess=guess, num_guesses=num)

@app.route('/take_turn', methods=['POST'])
def playing_game():
    num = session['num_left']
    secret_word = session['secret_word']
    guess = session['guess']
    
    letters = session['letters']
    

    if not game_over(num, secret_word, guess):

        letter = request.form.get('letter')

        # while letter in letter:
        #     letter = util.request_letter()

        letters.append(letter)

        indexes = find_letter_in_word(secret_word, letter)

        if indexes:
            guess = update_guess(guess,indexes, letter)
            session['guess'] = guess
            

        else:
            num -= 1
            session['num_left'] = num
        
        
        session['letters'] = letters

    guess_word = convert_to_string(guess)

    return render_template('game.html', guess=guess_word, missed=letters,num_guesses=num)

#############
# Helper Functions


def select_word(wordbook):
    """ Selects a psudo-random word from a Wordbook object
        Saves index used into db
        Returns a list object of word. ie. 'ant' = ['a','n','t']"""

    wordlist = wordbook.book.split()

    rand_num = random.randint(0, len(wordlist)-1)

    old_indexes = get_used_indexes(wordbook)

    while rand_num in old_indexes:
        rand_num = random.randint(0, len(wordlist)-1)

    new_index = Used_index(wordbook_id=wordbook.wordbook_id,
                            index_num=rand_num)

    db.session.add(new_index)
    db.session.commit()

    secret_word = list(wordlist[rand_num])

    return secret_word

def get_used_indexes(wordbook):
    """Finds all used indexes connected to wordbook record
        returns a set of all found index numbers"""

    indexes = Used_index.query.filter(Used_index.wordbook_id == wordbook.wordbook_id).all()

    used = set()

    for index in indexes:
        used.add(index.index_num)

    return used

def convert_to_string(char_list):
    """Takes a list of chars and returns as a string"""
    
    return ''.join(char_list)

def game_over(num_guesses, secret_word, guess):
    """Checks if game is over. Returns True if Over.
        False if not Over."""

    if num_guesses > 0 and secret_word != guess:
        return False

    return True

def find_letter_in_word(secret_word, letter):
    """ Looks for letter in secret_word
        Returns [] of matching indexes, Empty [] = None found """

    index = []

    for i, char in enumerate(secret_word):
        if char == letter:
            index.append(i)

    return index 

def update_guess(guess, indexes, letter):
    """ Replaces '_' with letter at indexes of guess 
        Returns updated guess """

    for i in indexes:
        guess[i] = letter

    return guess

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
