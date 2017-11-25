import random
import search
import math
import re
import nltk
import constants
import syllabifier
from nltk.corpus import brown
from nltk.util import bigrams


class Haiku(object):
    """Haiku class represents a haiku poem"""

    def __init__(self, text_file_name, selection_length=25, corpus_genre='religion'):
        file = open(text_file_name, 'r')
        text = file.read()
        file.close()

        self.originText = re.sub('[^a-zA-Z0-9\n\.]', ' ', text) #string
        self.chosen_lines_list = self.choose_lines_list(selection_length) #list of lists
        self.chosen_lines = self.choose_lines(selection_length) #string
        self.mainText = "" #string
        for word in self.chosen_lines:
            self.mainText += word.lower()
        self.words_in_chosen_text = [w.lower() for w in nltk.word_tokenize(self.mainText)] #list of words
        self.clean_words = clean_words(self.words_in_chosen_text) #list of words
        self.clean_text = re.sub('[^a-zA-Z]', ' ',self.mainText.replace(constants.FAKE_NEW_LINE, "")) #string
        self.poem = self.make_poem() #string

        # CORPUS ATTRIBUTES #
        self.corpus = brown.words(categories=corpus_genre)
        self.lc_corp = [w.lower() for w in self.corpus]
        self.common_bigrams = [(x, y) for (x, y) in bigrams(self.lc_corp)
                               if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT
                               and x in self.mainText and y in self.mainText]
        self.cfd = nltk.ConditionalFreqDist(self.common_bigrams)

    def choose_lines_list(self, num_lines):
        """returns list of lists with each sublist representing a line in the output
        int -> nested list

        Note: This is the majority of our run time because it iterates through the entire
        origin text several times. We should think about making it more efficient."""
        self.originText = self.originText.replace("\n", " " + constants.FAKE_NEW_LINE + " ")
        self.originText = self.originText.replace(" " + constants.FAKE_NEW_LINE + "  " + constants.FAKE_NEW_LINE + " ",
                                                  " " + constants.FAKE_NEW_LINE + " ")
        line = []
        lines = []
        words_in_text = [w.lower() for w in nltk.word_tokenize(self.originText)]
        for word in words_in_text:
            if word != constants.FAKE_NEW_LINE:
                line.append(word)
            else:
                lines.append(line)
                line = []
        chosen_lines = []
        start = random.randint(0,len(lines)-num_lines)
        lines_chosen = 0

        while lines_chosen < num_lines:
            if lines[start] is not []:
                chosen_lines.append(lines[start])
                lines_chosen += 1
                start += 1
            else:
                start += 1

        return chosen_lines

    def choose_lines(self, num_lines):
        """Returns chosen lines as text. We are primarily working with text strings, but
        we also need the text represented as a list of words to pull each word and a list
        of lists to represent each line. Hence we have a ton of different representations
        of the text
        int -> String"""
        lines = self.chosen_lines_list
        poem_line = ""
        poem_lines = ""
        for line in lines:
            for word in line:
                poem_line = poem_line + " " + word
            poem_lines = poem_lines + "\n" + poem_line
            poem_line = ""
        return poem_lines

    def make_poem(self):
        """Turns list of lists representing poem into an easy-to-read string
        None -> String"""
        poem_line = ""
        poem = ""
        poem_list = search.poem_searcher(self.clean_words, self.chosen_lines_list)
        for line in poem_list:
            for word in line:
                poem_line = poem_line + " " + word
            poem = poem + poem_line + "\n"
            poem_line = ""
        return poem


def clean_words(list_of_words):
    """Returns words without new line character
    list -> list"""
    words = []
    for word in list_of_words:
        if word != constants.FAKE_NEW_LINE:
            words.append(word)
    return words
