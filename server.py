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
    """Renders the homepage"""

    # Sets a bunch of session variables to none
    session['num_left'] = None
    session['letters'] = []
    session['guess'] =[]
    session['id'] = None
    session['secret_word'] = []
    return render_template('homepage.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Sets up the game and renders the gamepage"""
    
    # Gets the difficulty setting
    difficulty = request.form.get('difficulty')
    
    # Number of chances to guess the word
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
    """Selects a new word from the already generated wordbook
        renders the gamepage"""


    num = 6
    # set/reset session vars 
    session['num_left'] = num
    session['letters'] = []
    session['guess'] =[]
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
    """Handles the playing of the game"""

    # Retrives session variables
    num = session['num_left']
    secret_word = session['secret_word']
    guess = session['guess']
    
    letters = session['letters']
    
    #c Checks if the Game is over
    if not game_over(num, secret_word, guess):

        # Gets the data from the form
        letter = request.form.get('letter')
        letter = clean_data(letter)
        
        # Checks if player has entered that guess before
        if is_duplicate(letter, letters):

            # If dupicate guess, asks them to try again
            flash("You already tried that one.")
            guess_word = convert_to_string(guess)
            
            return render_template('game.html', 
                            guess=guess_word, 
                            missed=letters,
                            num_guesses=num)

        # Checks if player has only entered letters
        if not letter.isalpha():

            # If play entered non letters asks them to try again
            flash("You must enter only letters.")
            guess_word = convert_to_string(guess)
            
            return render_template('game.html', 
                            guess=guess_word, 
                            missed=letters,
                            num_guesses=num)
        
       # If player enters more that 1 letter
       # Checks if they guessed the word correctly
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
                # Wrong guess, lose a chance
                num -= 1
                session['num_left'] = num
        else:

            # If player only guesses 1 letter
            indexes = find_letter_in_word(secret_word, letter)

            # If letter matches found, update the guess word
            if indexes:
                guess = update_guess(guess,indexes, letter)
                session['guess'] = guess
                
            # No match, lose a chance
            else:
                num -= 1
                session['num_left'] = num
        
        # Adds guess to list, updates session var
        letters.append(letter)
        session['letters'] = letters

    # Varibles needed for template rendering
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
    """Takes a list of chars and returns as a string

        >>> a = ['d','o','g']
        >>> convert_to_string(a)
        'dog'
    """
    
    return ''.join(char_list)

def game_over(num_guesses, secret_word, guess):
    """Checks if game is over. Returns True if Over.
        False if not Over.

        >>> num = 0
        >>> secret = ['d','o','g']
        >>> guess = ['d', '_','_']
        >>> game_over(num, secret, guess)
        True
        >>> num = 4
        >>> secret = ['d','o','g']
        >>> guess = ['d', 'o','g']
        >>> game_over(num, secret, guess)
        True
        >>> num = 4
        >>> secret = ['d','o','g']
        >>> guess = ['d', '_','_']
        >>> game_over(num, secret, guess)
        False

        """

    if num_guesses > 0 and secret_word != guess:
        return False

    return True

def is_winner(num_guesses, secret_word, guess):
    """Checks if Player won. Returns True if Won.
        False if lost.

        >>> num = 4
        >>> secret = ['d','o','g']
        >>> guess = ['d', 'o','g']
        >>> is_winner(num, secret, guess)
        True
        >>> num = 0
        >>> secret = ['d','o','g']
        >>> guess = ['d', '_','_']
        >>> is_winner(num, secret, guess)
        False

        """

    if num_guesses > 0 and secret_word == guess:
        return True

    return False

def find_letter_in_word(secret_word, letter):
    """ Looks for letter in secret_word
        Returns [] of matching indexes, Empty [] = None found

        >>> secret = ['a','p','p','l','e']
        >>> letter = 'p'
        >>> find_letter_in_word(secret, letter)
        [1, 2]
        >>> secret = ['a','p','p','l','e']
        >>> letter = 'y'
        >>> find_letter_in_word(secret, letter)
        []

        """

    index = []

    for i, char in enumerate(secret_word):
        if char == letter:
            index.append(i)

    return index 

def update_guess(guess, indexes, letter):
    """ Replaces '_' with letter at indexes of guess 
        Returns updated guess 

        >>> guess = ['_']*5
        >>> letter = 'p'
        >>> idx = [1,2]
        >>> update_guess(guess, idx, letter)
        ['_', 'p', 'p', '_', '_']

        """

    for i in indexes:
        guess[i] = letter

    return guess

def clean_data(data):
    """Converts data to lowercase and removes extra spaces.
        Returns cleaned value.

        >>> temp = " thE "
        >>> clean_data(temp)
        'the'
     
        >>> caps = "THEIS"
        >>> clean_data(caps)
        'theis'
        """ 
    
    data = data.lower()
    data = data.strip()
    return data


def is_duplicate(data, used):
    """checks to see if the entered data has been entered before.
        Returns T if seen before. F if new.

        >>> data = 'p'
        >>> used = ['the', 'p', 'l','a']
        >>> is_duplicate(data, used)
        True
        >>> data = 'p'
        >>> used = ['the', 'l','a']
        >>> is_duplicate(data, used)
        False
        >>> data = 'the'
        >>> used = ['the', 'p', 'l','a']
        >>> is_duplicate(data, used)
        True
        >>> data = 'ham'
        >>> used = ['the', 'p', 'l','a']
        >>> is_duplicate(data, used)
        False

        """

    old = set(used)

    if data in old:
        return True

    return False

def words_match(secret_word, word):
    """Takes secret_word(as a list) word(as a string).
        Returns True if they match. False if they dont.

        >>> secret = ['c','a','t']
        >>> word = 'cat'
        >>> words_match(secret, word)
        True
        >>> secret = ['c','a','t']
        >>> word = 'got'
        >>> words_match(secret, word)
        False

        """

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
