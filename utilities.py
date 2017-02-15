
def print_word(word):
    """Takes a list of chars and prints as a string"""
    print ''.join(word)

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
