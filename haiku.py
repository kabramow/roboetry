import random
import random
import nltk
from nltk.corpus import brown
from nltk.corpus import cmudict
from nltk.util import bigrams
pro = cmudict.dict()                                                                                                    #grabbing a dictionary that wil allow us to look up syllables



class Haiku(object):
    """Haiku class represents a haiku poem"""

    def __init__(self, textFileName, corpus_genre = 'religion'):
        self.originText = open(textFileName, 'r').read()                                                                #entire text as a string
        self.mainText = self.chooseLines(25)                                                                            #text we are working from
        self.wordsInChosenText = [w.lower() for w in nltk.word_tokenize(self.mainText)]                                 #list of words in our text
        self.corpus = brown.words(categories=corpus_genre)                                                              #training corpus (need to implement)
        self.lc_corp = [w.lower() for w in self.corpus]                                                                 # making corpus all lowercase (shorthand for loop is basically like map in Racket)
        self.common_bigrams = [(x, y) for (x, y) in bigrams(self.lc_corp)
                               if x in pro and y in pro and x in self.mainText and y in self.mainText]                  # only using words we can look up in syllable dict and are in our text
        self.cfd = nltk.ConditionalFreqDist(self.common_bigrams)                                                        #a dictionary representing continuations of words
        self.syllable_list = self.get_syllable_list()                                                                   #a list of lists - one list of words for each syllable length 1-7
        self.endLocationOfLineOne = 0                                                                                   #the index in self.mainText of the last word of line 1 in poem
        self.endLocationOfLineTwo = 0                                                                                   #the index in self.mainText of the last word of line 2 in poem
        self.poem = self.make_poem()




    def chooseLines(self, num_lines):
        """Given a number of lines, returns a subtext of that amount of lines
        int -> String"""

        lines = nltk.sent_tokenize(self.originText)                                                                     #occasionally breaks if we use .split instead of tokenize
        start_point = random.randint(0, len(lines)-num_lines)                                                           #right now our starting point is completely random
        chosenLinesOfText = ""
        line_count = 0
        for i in range(start_point, start_point + 100):                                                                 #a for loop collecting subsequent lines
            if line_count < num_lines:
                if lines[i] != "":
                    chosenLinesOfText += lines[i]
                    chosenLinesOfText += " \n "
                    line_count += 1
            else:
                return chosenLinesOfText



    def get_words_of_syllable_length(self, num):
        """Given a text and a number of syllables, returns list of words
        containing that amount of syllables
        String, int -> list"""

        word_list = []
        for word in self.wordsInChosenText:
            if word in pro:                                                                                             #making sure it's possible to look up syllable count in dictionary
                if get_syllables(word) == num:
                    word_list.append(word)
            else:
                pass
        return word_list



    def get_syllable_list(self):
        """Returns one list of 7 sublists, each sublist containing all words
        present within haiku's text that contain certain number of syllables
        i.e. position 0 of return list contains all words in text with a syllable
        count of 1. Position 6 has all words with syllable count of 7
        None -> Nested list"""

        sorted_list_of_syllables = [];
        for i in range(7):
            sy = self.get_words_of_syllable_length(i + 1)
            sorted_list_of_syllables.append(sy)
        return sorted_list_of_syllables



    def make_random_line(self, numOfSyllables, pos=0, lineNumber = 1):
        """Given a number of syllables, creates a haiku line of that syllable length
        int -> String"""
        word_is_usable = False
        while not word_is_usable:
            new_number = random.randrange(numOfSyllables) + 1                                                           # pick a random number of syllables for the word
            if self.syllable_list[new_number - 1]:
                tentative_word = random.choice(self.syllable_list[new_number - 1])                                      # grab a word with that amount of random syllables
                tentative_word_pos = self.wordsInChosenText.index(tentative_word)
                if pos < tentative_word_pos < pos+(len(self.wordsInChosenText)/5):                                      #this sucks lol - it's basically a search that just picks random things until they work
                    new_word = tentative_word
                    break
        currentIndex = self.wordsInChosenText.index(new_word)
        remaining = numOfSyllables - new_number
        if remaining == 0:
            word_list = new_word
            if lineNumber == 1:
                self.endLocationOfLineOne = currentIndex
            if lineNumber == 2:
                self.endLocationOfLineTwo = currentIndex
        else:
            word_list = new_word + " " + self.make_random_line(remaining, currentIndex, lineNumber)                     # yay recursion!!!

        return word_list




    def make_poem(self):
        """Returns haiku of 5-7-5
        None -> String"""
        lineOne = self.make_random_line(5,0,1) + "\n"
        lineTwo = self.make_random_line(7,self.endLocationOfLineOne,2) + "\n"
        lineThree = self.make_random_line(5,self.endLocationOfLineTwo,3)
        poem =  lineOne+lineTwo+lineThree
        return poem



    def body_generator(self):
        """docString
        purpose statement
        None -> String"""

        # text.replace('\n', "</p><p id=\"blackout\">")
        text_words = self.wordsInChosenText
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
def get_syllables(word):
    """given a word, returns the number of syllables in the word

    string -> int"""

    syllables = []
    if word in pro:
        pronunciation = pro[word]                                                                                       #a list of phones
    else:
        pronunciation = ["not found"]
    for i in pronunciation[0]:
        if i[-1].isdigit():                                                                                             #number represents a syllable
            syllables.append(i)
    num_syllables = len(syllables)
    return num_syllables




def main():
    fairy_tales = Haiku("ft.txt")
    #print(fairy_tales.mainText)
    print(fairy_tales.poem)
    fairy_tales.display_poem("test")

main()
