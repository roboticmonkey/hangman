This is the README for the Hangman game.

Files need to run the game:
* model.py
* server.py
* static/
    * 0.svg
    * 1.svg
    * 2.svg
    * 3.svg
    * 4.svg
    * 5.svg
    * 6.svg
    * stylesheet.css
* templates/
    * game.html
    * homepage.html
* requirements.txt

To build the game from the command line:

* You will need to be connected to the internet

1. pip install the list of dependencies found in requirements.txt
2. create a postgresql database named hangman
3. run  python model.py" to build the required tables in the db.
4. run python server.py to start the local server
5. Open a web browers and navigate to the address the server is running on.
    my computer shows the address as http://127.0.0.1:5000/ 
    Its possible yours is running on a different port

Playing the game:

* Select the difficulty level and click Submit
* You can enter 1 letter at a time or you can try guessing the whole word
* Each wrong guess reveals another part of the stickfigure
* When word is guessed or player runs out of guesses, player can choose
    to get another word or start a new game.

The tech stack of this project is:
* Python
* Flask
* Flask SQLALchemy, SQLAlchemy
* Postgresql
* Bootstrap for quick style

I first wrote a basic version of the hangman game entirely in Python using OOP
and then converted it to a Python/Flask web app using a MVC structure. The Model
is my model.py, the Views are in the templates/, and the Controller is the server.py.

The basic flow is:

To create the dictionary of words, my app hits the dictionary api and saves the 
string of words into the db. That way when a player wants a new word, the 
dictionary is retrieved from the db instead of hitting the api again.

To get a word, I tokenize the dictionary string into an array. I used a pysudo-random
number to index the array and retrieve a word. I save this index in the db so that
future index can be checked against a list of previous indexes - therefore not repeating
a word.

While playing the app does all validation on the server-side. It checks if a letter or
letters were given and if the player has guessed that letter or word before. 
Duplicate guesses are not counted against the player and they are given another
chance to guess. A correct guess will update the word the player is trying to guess.
A wrong guess will lose a chance.

The game ends when the player guesses the word before the player runs out of chances
or they run out of chances.

Extra features I have added:
* Ability to choose a difficulty level of the words
* Ability to guess the whole word at once as well as 1 letter at a time
* Ability to pick another random word from the dictionary without having to hit the 
API again
* Made some simple vector graphics to make the game more enjoyable to play



