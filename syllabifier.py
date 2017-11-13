import constants


def get_syllables(word):
    """given a word, returns the number of syllables in the word
    string -> int"""

    syllables = []
    if word in constants.PRONUNCIATION_DICT:
        pronunciation = constants.PRONUNCIATION_DICT[word]                                                              #a list of phones
    else:
        pronunciation = ["not found"]
    for i in pronunciation[0]:
        if i[-1].isdigit():                                                                                             #number represents a syllable
            syllables.append(i)
    num_syllables = len(syllables)
    return num_syllables


def get_words_of_syllable_length(num, words_in_chosen_text):
    """Given a text and a number of syllables, returns list of words
    containing that amount of syllables
    String, int -> list"""

    word_list = []
    for word in words_in_chosen_text:
        if word in constants.PRONUNCIATION_DICT:    #making sure it's possible to look up syllable count in dictionary
            if get_syllables(word) == num:
                word_list.append(word)
        else:
            pass
    return word_list

