import constants


def get_syllables(word):
    """given a word, returns the number of syllables in the word
    string -> int"""

    syllables = []
    if word in constants.PRONUNCIATION_DICT:
        # a list of phones
        pronunciation = constants.PRONUNCIATION_DICT[word]
    else:
        pronunciation = ["not found"]
    for i in pronunciation[0]:
        # number represents a syllable
        if i[-1].isdigit():
            syllables.append(i)
    num_syllables = len(syllables)
    return num_syllables


def get_words_of_syllable_length(num, words_in_chosen_text):
    """Given a text and a number of syllables, returns list of words
    containing that amount of syllables
    String, int -> list"""

    word_list = []
    for word in words_in_chosen_text:
        # making sure it's possible to look up syllable count in dictionary
        if word in constants.PRONUNCIATION_DICT:
            if get_syllables(word) == num:
                word_list.append(word)
        else:
            pass
    return word_list


def get_syllable_list(words_in_chosen_text):
    """Returns one list of 7 sub lists, each sublist containing all words
    present within haiku's text that contain certain number of syllables
    i.e. position 0 of return list contains all words in text with a syllable
    count of 1. Position 6 has all words with syllable count of 7
    None -> Nested list"""

    sorted_list_of_syllables = []
    for i in range(7):
        sy = get_words_of_syllable_length(i + 1, words_in_chosen_text)
        sorted_list_of_syllables.append(sy)
    return sorted_list_of_syllables
