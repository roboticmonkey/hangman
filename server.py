""" Server File """

from jinja2 import StrictUndefined
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "something-secret"

app.jinja_env.undifined = StrictUndefined

########
# Routes

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/start')
def start_game():
    word = '______'
    return render_template('homepage.html', word=word)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # app.debug = False

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
