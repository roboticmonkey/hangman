import wordbook
import utilities as util

# Create a list of words to select from
dictionary = wordbook.Wordbook()
dictionary.create_wordbook()

secret_word = dictionary.select_word()
print secret_word

guess = ['_'] * len(secret_word)
print guess

print util.convert_to_string(guess)

number_of_guesses = 6
missed = []
guesses = set()


while not util.game_over(number_of_guesses, secret_word, guess):
    print number_of_guesses, "guess left."
    if missed:
        print "already guessed", missed

   
    letter = util.request_letter()

    while letter in guesses:

        letter = util.request_letter()

    guesses.add(letter)

    indexes = util.find_letter_in_word(letter, secret_word)

    if indexes:
        guess = util.update_guess(indexes, letter, guess)
        print util.convert_to_string(guess)
    else:
        number_of_guesses -=1
        missed.append(letter)
      
s = util.convert_to_string(guess)
if number_of_guesses > 0:
    print "You won! The word was %s!" %(s)
else:
    print "Too Bad!"