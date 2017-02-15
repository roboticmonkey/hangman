
def convert_to_string(word):
    """Takes a list of chars and returns as a string"""
    
    return ''.join(word)


def request_letter():
    """ Requests a letter and Returns a valid lowercase letter between
        a-z"""
    a = unicode('a')
    z = unicode('z')
    invalid = True

    while invalid:
        letter = unicode(raw_input("Enter a Letter: ")).lower()

        if letter >= a and letter <= z:
            invalid = False

    return letter

def find_letter_in_word(letter, secret_word):
    """ Looks for letter in word
        Returns [] of matching indexes, Empty [] = Not found """

    index = []

    for i, char in enumerate(secret_word):
        if char == letter:
            index.append(i)

    return index

def update_guess(indexes, letter, guess):
    """ Replaces '_' with letter at indexes of guess 
        Returns updated guess """

    for i in indexes:
        guess[i] = letter

    return guess

def game_over(num_guesses, secret_word, guess):

    if num_guesses > 0 and secret_word != guess:
        return False

    return True


