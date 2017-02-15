import wordbook


# Create a list of words to select from
dictionary = wordbook.Wordbook()
dictionary.create_wordbook()

secret_word = dictionary.select_word()
print secret_word

