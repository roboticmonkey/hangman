import hangman
import utilities as util

game = hangman.Hangman()

game.new_game()


print util.convert_to_string(game.secret_word)

print util.convert_to_string(game.guess)


while not game.game_over():
    print game.num_guesses, "guesses left."
    if game.missed_letters:
            print "already guessed", util.convert_to_string(game.missed_letters)

    letter = util.request_letter()

    while letter in game.guesses:
        letter = util.request_letter()

    game.guesses.add(letter)

    indexes = game.find_letter_in_word(letter)

    if indexes:
        game.update_guess(indexes, letter)
        print util.convert_to_string(game.guess)

    else:
        game.update_num_guesses()
        game.update_missed(letter)

      
s = util.convert_to_string(game.guess)
if game.num_guesses > 0:
    print "You won! The word was %s!" %(s)
else:
    print "Too Bad!"


