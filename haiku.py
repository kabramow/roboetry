import random
import nltk
import constants
import syllabifier
from nltk.corpus import brown
from nltk.util import bigrams


class Haiku(object):
    """Haiku class represents a haiku poem"""

    def __init__(self, text_file_name, corpus_genre='religion'):
        # entire text as a string
        self.originText = open(text_file_name, 'r').read()
        # text we are working from
        self.mainText = self.choose_lines(15)
        # list of words in our text
        self.words_in_chosen_text = [w.lower() for w in nltk.word_tokenize(self.mainText)]
        # training corpus (need to implement)
        self.corpus = brown.words(categories=corpus_genre)
        # making corpus all lowercase (shorthand for loop is basically like map in Racket)
        self.lc_corp = [w.lower() for w in self.corpus]
        # only using words we can look up in syllable dict and are in our text
        self.common_bigrams = [(x, y) for (x, y) in bigrams(self.lc_corp)
                               if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT
                               and x in self.mainText and y in self.mainText]
        # a dictionary representing continuations of words
        self.cfd = nltk.ConditionalFreqDist(self.common_bigrams)
        # a list of lists - one list of words for each syllable length 1-7
        self.syllable_list = syllabifier.get_syllable_list(self.words_in_chosen_text)
        # the index in self.mainText of the last word of line 1 in poem
        self.end_location_of_line_one = 0
        # the index in self.mainText of the last word of line 2 in poem
        self.end_location_of_line_two = 0
        self.poem = self.make_poem()

    def choose_lines(self, num_lines):
        """Given a number of lines, returns a subtext of that amount of lines
        int -> String"""
        self.originText = self.originText.replace("\n", " " + constants.FAKE_NEW_LINE + " ")
        self.originText = self.originText.replace(" " + constants.FAKE_NEW_LINE + "  " + constants.FAKE_NEW_LINE + " ",
                                                  " " + constants.FAKE_NEW_LINE + " ")
        # occasionally breaks if we use .split instead of tokenize
        lines = nltk.sent_tokenize(self.originText)

        # right now our starting point is completely random
        start_point = random.randint(100, len(lines)-200)

        chosen_lines_of_text = ""
        line_count = 0
        # a for loop collecting subsequent lines
        for i in range(start_point, start_point + 100):
            if line_count < num_lines:
                if lines[i] != "":
                    chosen_lines_of_text += " " + lines[i]
                    # chosen_lines_of_text += " " + constants.FAKE_NEW_LINE + " "
                    line_count += 1
            else:
                return chosen_lines_of_text

    def make_random_line(self, num_of_syllables, pos=0, line_number=1):
        """Given a number of syllables, creates a haiku line of that syllable length
        int -> String"""
        word_is_usable = False
        while not word_is_usable:
            # pick a random number of syllables for the word
            new_number = random.randrange(num_of_syllables) + 1
            if self.syllable_list[new_number - 1]:
                # grab a word with that amount of random syllables
                tentative_word = random.choice(self.syllable_list[new_number - 1])
                tentative_word_pos = self.words_in_chosen_text.index(tentative_word)
                # this sucks lol - it's basically a search that just picks random things until they work
                if pos < tentative_word_pos < pos+(len(self.words_in_chosen_text)/5):
                    new_word = tentative_word
                    break
        current_index = self.words_in_chosen_text.index(new_word)
        remaining = num_of_syllables - new_number
        if remaining == 0:
            word_list = new_word
            if line_number == 1:
                self.end_location_of_line_one = current_index
            if line_number == 2:
                self.end_location_of_line_two = current_index
        else:
            # yay recursion!!!
            word_list = new_word + " " + self.make_random_line(remaining, current_index, line_number)

        return word_list

    def make_poem(self):
        """Returns haiku of 5-7-5
        None -> String"""
        line_one = self.make_random_line(5, 0, 1) + "\n"
        line_two = self.make_random_line(7, self.end_location_of_line_one, 2) + "\n"
        line_three = self.make_random_line(5, self.end_location_of_line_two, 3)
        poem = line_one + line_two + line_three
        return poem


def make_haiku(text_file_name):
    return Haiku(text_file_name)

