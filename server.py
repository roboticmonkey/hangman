""" Server File """

from jinja2 import StrictUndefined
from flask import Flask, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

import hangman
import utilities as util


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
    game = hangman.Hangman()
    game.new_game()
    num = game.num_guesses
    guess = util.convert_to_string(game.guess)
    


    return render_template('game.html', guess=guess, num_guesses=num)

@app.route('/take_turn', methods=['POST'])
def playing_game():
    while not game.game_over():

        letter = request.form.get('letter')

        # while letter in game.guesses:
        #     letter = util.request_letter()

        game.guesses.add(letter)

        indexes = game.find_letter_in_word(letter)

        if indexes:
            game.update_guess(indexes, letter)
            

        else:
            game.update_num_guesses()
            game.update_missed(letter)


    return render_template('game.html', guess=guess, missed=missed)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # app.debug = False

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
