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
        try:
            if text_file_name.find(".txt") != -1:
                file = open(text_file_name, 'r')
                text = file.read()
                file.close()
            else:
                print("Invalid File - need a txt file")
                raise Exception("Invalid File")
        except:
            print("Unable to read file, Rootabaga Stories used instead")
            file = open("rootabaga_stories.txt", 'r')
            text = file.read()
            file.close()

        self.originText = re.sub('[^a-zA-Z0-9\n.]', ' ', text)  # string
        self.chosen_lines_list = self.choose_lines_list(selection_length)  # list of lists
        self.chosen_lines = self.choose_lines()  # string
        self.mainText = ""  # string
        for word in self.chosen_lines:
            self.mainText += word.lower()
        self.words_in_chosen_text = [w.lower() for w in nltk.word_tokenize(self.mainText)]  # list of words
        self.clean_words = clean_words(self.words_in_chosen_text)  # list of words
        self.clean_text = re.sub('[^a-zA-Z]', ' ',self.mainText.replace(constants.FAKE_NEW_LINE, ""))  # string

        # CORPUS ATTRIBUTES #
        self.corpus = brown.words(categories=corpus_genre)
        self.lc_corp = [w.lower() for w in self.corpus]
        self.common_bigrams = [(x, y) for (x, y) in bigrams(self.lc_corp)
                               if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT
                               and x in self.mainText and y in self.mainText]
        self.cfd = nltk.ConditionalFreqDist(self.common_bigrams)
        self.poem = self.make_poem()  # string

    def choose_lines_list(self, num_lines):
        """returns list of lists with each sublist representing a line in the output
        int -> nested list"""

        lines = self.originText.split("\n")
        start = random.randint(0, len(lines) - num_lines)
        lines_chosen = 0
        temp_chosen_lines = []

        while lines_chosen < num_lines:
            if lines[start] is not '':
                temp_chosen_lines.append(lines[start])
                lines_chosen += 1
                start += 1
            else:
                start += 1

        chosen_lines = []
        for line in temp_chosen_lines:
            updated_line = [w.lower() for w in nltk.word_tokenize(line)]
            chosen_lines.append(updated_line)

        return chosen_lines

    def choose_lines(self):
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
        poem_list = search.poem_searcher(self, self.clean_words, self.chosen_lines_list)
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
