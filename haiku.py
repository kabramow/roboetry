import random
import nltk
##nltk.download('cmudict')
##nltk.download('brown')
import constants
import syllabifier
from nltk.corpus import brown
from nltk.corpus import cmudict

from nltk.util import bigrams


class Haiku(object):
    """Haiku class represents a haiku poem"""

    def __init__(self, text_file_name, corpus_genre='religion'):
        self.originText = open(text_file_name, 'r').read()                                                              #entire text as a string
        self.mainText = self.choose_lines(25)                                                                           #text we are working from
        self.words_in_chosen_text = [w.lower() for w in nltk.word_tokenize(self.mainText)]                                 #list of words in our text
        self.corpus = brown.words(categories=corpus_genre)                                                              #training corpus (need to implement)
        self.lc_corp = [w.lower() for w in self.corpus]                                                                 # making corpus all lowercase (shorthand for loop is basically like map in Racket)
        self.common_bigrams = [(x, y) for (x, y) in bigrams(self.lc_corp)
                               if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT and x in self.mainText and y in self.mainText]                  # only using words we can look up in syllable dict and are in our text
        self.cfd = nltk.ConditionalFreqDist(self.common_bigrams)                                                        #a dictionary representing continuations of words
        self.syllable_list = self.get_syllable_list()                                                                   #a list of lists - one list of words for each syllable length 1-7
        self.endLocationOfLineOne = 0                                                                                   #the index in self.mainText of the last word of line 1 in poem
        self.endLocationOfLineTwo = 0                                                                                   #the index in self.mainText of the last word of line 2 in poem
        self.poem = self.make_poem()

    def choose_lines(self, num_lines):
        """Given a number of lines, returns a subtext of that amount of lines
        int -> String"""

        lines = nltk.sent_tokenize(self.originText)                                                                     #occasionally breaks if we use .split instead of tokenize
        start_point = random.randint(0, len(lines)-num_lines)                                                           #right now our starting point is completely random
        chosen_lines_of_text = ""
        line_count = 0
        for i in range(start_point, start_point + 100):                                                                 #a for loop collecting subsequent lines
            if line_count < num_lines:
                if lines[i] != "":
                    chosen_lines_of_text += lines[i]
                    chosen_lines_of_text += " \n "
                    line_count += 1
            else:
                return chosen_lines_of_text

    def get_syllable_list(self):
        """Returns one list of 7 sub lists, each sublist containing all words
        present within haiku's text that contain certain number of syllables
        i.e. position 0 of return list contains all words in text with a syllable
        count of 1. Position 6 has all words with syllable count of 7
        None -> Nested list"""

        sorted_list_of_syllables = []
        for i in range(7):
            sy = syllabifier.get_words_of_syllable_length(i + 1, self.words_in_chosen_text)
            sorted_list_of_syllables.append(sy)
        return sorted_list_of_syllables

    def make_random_line(self, num_of_syllables, pos=0, line_number=1):
        """Given a number of syllables, creates a haiku line of that syllable length
        int -> String"""
        word_is_usable = False
        while not word_is_usable:
            new_number = random.randrange(num_of_syllables) + 1                                                         # pick a random number of syllables for the word
            if self.syllable_list[new_number - 1]:
                tentative_word = random.choice(self.syllable_list[new_number - 1])                                      # grab a word with that amount of random syllables
                tentative_word_pos = self.words_in_chosen_text.index(tentative_word)
                if pos < tentative_word_pos < pos+(len(self.words_in_chosen_text)/5):                                      #this sucks lol - it's basically a search that just picks random things until they work
                    new_word = tentative_word
                    break
        current_index = self.words_in_chosen_text.index(new_word)
        remaining = num_of_syllables - new_number
        if remaining == 0:
            word_list = new_word
            if line_number == 1:
                self.endLocationOfLineOne = current_index
            if line_number == 2:
                self.endLocationOfLineTwo = current_index
        else:
            word_list = new_word + " " + self.make_random_line(remaining, current_index, line_number)                   # yay recursion!!!

        return word_list

    def make_poem(self):
        """Returns haiku of 5-7-5
        None -> String"""
        line_one = self.make_random_line(5, 0, 1) + "\n"
        line_two = self.make_random_line(7, self.endLocationOfLineOne, 2) + "\n"
        line_three = self.make_random_line(5, self.endLocationOfLineTwo, 3)
        poem = line_one + line_two + line_three
        return poem

    def body_generator(self):
        """docString
        purpose statement
        None -> String"""

        # text.replace('\n', "</p><p id=\"blackout\">")
        text_words = self.words_in_chosen_text
        poem = nltk.word_tokenize(self.poem)
        out_text = ""
        for word in text_words:
            if len(poem) != 0:
                if word == poem[0]:
                    poem = poem[1:]
                    out_text += "<span id=\"poem\">" + word + "</span>" + " "
                elif word == "\n":
                    out_text += "</p><p>"
                else:
                    out_text += word + " "
            elif word == "\n":
                out_text += "</p><p>"
            else:
                out_text += word + " "

        return out_text

    def display_poem(self, program):
        """Given a file name, creates and opens html display of poem
        String -> None"""

        from webbrowser import open_new_tab

        filename = program + '.html'
        f = open(filename, 'w')

        wrapper = """<html>
        <head>
            <title>%s output</title>
            <style>
                body {
                    font-family: Georgia;
                }            
                #poem {
                    background-color: white;
                    color: black;
                }
                #blackout {
                    background-color: #101010;
                    color: black;
                }
            </style>
        </head>
            <body>
                <p id=\"title\">
                    Poem Generated By 
                    <a href=\"https://github.com/kabramow/roboetry\">Roboetry</a> 
                    from *****INSERT REF TO SOURCE MATERIAL
                </p>
                <div id=\"blackout\"><p>%s</p></div>
            </body>
        </html>"""

        whole = wrapper % (program, self.body_generator())
        f.write(whole)
        f.close()

        open_new_tab(filename)


#Note: get_syllables() is a separate function not included in the Haiku class



def main():
    fairy_tales = Haiku("ft.txt")
    #print(fairy_tales.mainText)
    print(fairy_tales.poem)
    fairy_tales.display_poem("test")


main()
