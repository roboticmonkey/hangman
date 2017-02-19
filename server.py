""" Server File """

from jinja2 import StrictUndefined
from flask import Flask, render_template, session, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import random

import utilities as util
from model import connect_to_db, Wordbook, db, Used_index, generate_wordlist


app = Flask(__name__)

app.secret_key = "something-secret"

app.jinja_env.undifined = StrictUndefined

########
# Routes

@app.route('/')
def index():
    session['num_left'] = None
    session['letters'] = []
    session['guess'] =[]
    session['id'] = None
    session['secret_word'] = []
    return render_template('homepage.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    
    difficulty = request.form.get('difficulty')
    num = 6
    # set/reset session vars 
    session['num_left'] = num

    # Generate the wordlist via api
    words = generate_wordlist(difficulty)
    
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

@app.route('/new_word')
def new_word():
    
    num = 6
    # set/reset session vars 
    session['num_left'] = num
    session['letters'] = []
    session['guess'] =[]
    # session['id'] = None
    session['secret_word'] = []

    # Retrive wordbook from db
    old_book = Wordbook.query.filter_by(wordbook_id=session['id']).first()

    # Select a new secret word from wordbook
    secret_word = select_word(old_book)
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
        letter = clean_data(letter)
        
        if is_dupilicate(letter, letters):
            flash("You already tried that one.")
            guess_word = convert_to_string(guess)
            
            return render_template('game.html', 
                            guess=guess_word, 
                            missed=letters,
                            num_guesses=num)

        if not letter.isalpha():
            flash("You must enter only letters.")
            guess_word = convert_to_string(guess)
            
            return render_template('game.html', 
                            guess=guess_word, 
                            missed=letters,
                            num_guesses=num)
        
       
        if len(letter) > 1:
            if words_match(secret_word, letter):
                guess = letter
                over = True
                winner = True

                return render_template('game.html', 
                                guess=guess, 
                                missed=letters,
                                num_guesses=num,
                                win=winner,
                                over=over)
            else:

                num -= 1
                session['num_left'] = num
        else:

            indexes = find_letter_in_word(secret_word, letter)

            if indexes:
                guess = update_guess(guess,indexes, letter)
                session['guess'] = guess
                

            else:
                num -= 1
                session['num_left'] = num
            
        letters.append(letter)
        session['letters'] = letters

    guess_word = convert_to_string(guess)

    over = game_over(num, secret_word, guess)
    winner = is_winner(num, secret_word, guess)
    secret = convert_to_string(secret_word)

    return render_template('game.html', 
                            guess=guess_word, 
                            missed=letters,
                            num_guesses=num,
                            win=winner,
                            over=over,
                            secret=secret)

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

def is_winner(num_guesses, secret_word, guess):
    """Checks if Player won. Returns True if Won.
        False if lost."""

    if num_guesses > 0 and secret_word == guess:
        return True

    return False

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

def clean_data(data):
    
    data = data.lower()
    data = data.strip()
    return data


def is_dupilicate(data, used):
    """checks to see if the entered data has been entered before.
        Returns T if seen before. F if new."""

    old = set(used)

    if data in old:
        return True

    return False

def words_match(secret_word, word):
    """Takes secret_word(as a list) word(as a string).
        Returns True if they match. False if they dont."""

    secret = convert_to_string(secret_word)
    if secret == word:
        return True
    else:
        return False

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
