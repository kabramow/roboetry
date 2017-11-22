import syllabifier
import brown_corpus_texts
from queue import PriorityQueue
import random
import math
import constants
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import brown
from nltk.util import bigrams

def poem_searcher(haiku, search_space, p_search_lines):
    """Returns a 5-7-5 Haiku based off of heuristics
    String, list -> list"""

    frontier = PriorityQueue()
    pass_through = 0
    num_syllables = 5
    search_lines = p_search_lines
    start_of_line = False #tells us if the word we are picking is the first in a line
    end_of_line = False #tells us if the word we are picking is the end of the line
    poem = [[], [], []]

    # CODE FOR PICKING START WORD (RANDOM)
    # start word must be towards beginning of text
    updated_search_space = []

    stopWords = set(stopwords.words('english'))

    for w in search_space:
        if w not in stopWords:
            updated_search_space.append(w)

    #Choosing first word -> picked based from first part of text, favor words that have
    #a lot of potential continuations
    first_word_search_space = updated_search_space[:int(len(updated_search_space) / 5)]
    num_next = [(len(haiku.cfd[x]), x) for x in haiku.cfd]
    sorted_next = sorted(num_next) #list of continuation words
    first_word = sorted_next[-1][1] #this will be the word with the most continuation words
    i=1
    while first_word not in first_word_search_space and constants.PRONUNCIATION_DICT:
        first_word = sorted_next[-i][1]
        i+=1

    # update the number of syllables left we have to work with
    syll_remaining = num_syllables - syllabifier.get_syllables(first_word)
    # append our chosen word to the corresponding line of our poem
    poem[pass_through].append(first_word)
    # add our first word to the frontier
    frontier.put((heuristic(haiku, first_word, first_word, search_lines, start_of_line), first_word))

    finished = False

    while not finished:
        # checking if we've finished all 3 lines of the haiku
        if pass_through == 2 and syll_remaining == 0:
            finished = True
            break
        # checking if we're done with the first line: if so, we need to start on a new line with 7 syllables
        elif pass_through == 0 and syll_remaining == 0:
            syll_remaining = 7
            pass_through = 1
            start_of_line = True
        # checking if we're done with the second line: if so, we need to start on a new line with 5 syllables
        elif pass_through == 1 and syll_remaining == 0:
            syll_remaining = 5
            pass_through = 2
            start_of_line = True
        else:
            start_of_line = False


        index_of_current_word = updated_search_space.index(first_word)
        #We need to reference individual words, but also whole lines to know what position
        #we are at in the html output. Rather than continually changing between data structures
        #(i.e. between a regular list and a nested list), we keep track of both cocurrently
        #so that we may rather reference which ever one we need at the moment
        updated_search_space = updated_search_space[index_of_current_word + 1:]
        search_lines = update_search_lines(search_lines, first_word)


        # UPDATING THE FRONTIER
        for neighbor in get_neighbors_list(first_word, updated_search_space):
            if neighbor in constants.PRONUNCIATION_DICT and syllabifier.get_syllables(neighbor) <= syll_remaining:
                # neighbors = all possible words, frontier = usable words, with heuristic values
                frontier.put((heuristic(haiku, first_word, neighbor, search_lines, start_of_line), neighbor))

        if frontier.queue:
            # grab first word in Priority Queue - i.e. WORD WITH LOWEST HEURISTIC
            first_word = sorted(list(frontier.queue))[0][1]
        else:
            break

        # RESET FRONTIER - the word that we choose eliminates a lot of words currently in the frontier,
        # so it is easy to remove all and then add again the valid words as the neighbors of the new word
        frontier = PriorityQueue()
        syll_remaining -= syllabifier.get_syllables(first_word)
        poem[pass_through].append(first_word)

    if finished == False:
        print("Syllable requirements not met.")
        return poem

    return poem



def update_search_lines(search_lines, p_word):
    """Keeps track of what line we are in in the html output
    nested list, string -> nested list"""
    index_to_cut = None
    row_count = 0
    for line in search_lines:
        for word in line:
            if word == p_word:
                y_to_cut = line.index(word)
                index_to_cut = row_count
                break
        row_count += 1
        if index_to_cut != None:
            break

    return_lines = search_lines[index_to_cut:]
    return_lines[0] = return_lines[0][y_to_cut:]
    return return_lines



def get_neighbors_list(word, list):
    """returns words following given word
    string, list -> list"""
    neighbors = list[0:int(len(list)/3)]

    return neighbors



def distance_heuristic(word1, word2, search_lines):
    """returns 'euclidean distance' of two words in html output
    string, string, nested list -> int"""
    val = 0
    xpos1 = None
    ypos1 = None
    xpos2 = None
    ypos2 = None
    row_count1 = 0
    row_count2 = 0

    for row in search_lines:
        for word in row:
            if word == word1:
                xpos1 = row_count1
                ypos1 = row.index(word)
                break
        row_count1+=1
        if xpos1 != None and ypos1 != None:
            break

    for row in search_lines:
        for word in row:
            if word == word2:
                xpos2 = row_count2
                ypos2 = row.index(word)
                break
        row_count2+=1
        if xpos2 != None and ypos2 != None:
            break

    if word1 == word2:
        return 5
    val = math.sqrt(math.pow((xpos2 - xpos1), 2) + math.pow((ypos2 - ypos1),2))
    return val


def continuation_heuristic(haiku, word1, word2, search, start_of_line):
    val = 100 #place holder value

    #using several corpuses (example texts), pulls words in text that follow
    #our already chosen word, word1
    continuation_words = haiku.cfd[word1]
    lore_words = brown_corpus_texts.lore_cfd[word1]
    fiction_words = brown_corpus_texts.fiction_cfd[word1]
    romance_words = brown_corpus_texts.romance_cfd[word1]
    mystery_words = brown_corpus_texts.mystery_cfd[word1]
    humor_words = brown_corpus_texts.humor_cfd[word1]
    sf_words = brown_corpus_texts.sf_cfd[word1]
    adventure_words = brown_corpus_texts.adventure_cfd[word1]

    #If our tentative word, word2, follows word1 in our example texts,
    #make our heuristic value be the likelihood/probability that word2
    #follows word1 according to our training texts
    if word2 in continuation_words:
        val = haiku.cfd[word1].freq(word2)
    if word2 in lore_words:
        val = brown_corpus_texts.lore_cfd[word1].freq(word2)
    if word2 in fiction_words:
        val = brown_corpus_texts.fiction_cfd[word1].freq(word2)
    if word2 in romance_words:
        val = brown_corpus_texts.romance_cfd[word1].freq(word2)
    if word2 in mystery_words:
        val = brown_corpus_texts.mystery_cfd[word1].freq(word2)
    if word2 in adventure_words:
        val = brown_corpus_texts.adventure_cfd[word1].freq(word2)
    if word2 in humor_words:
        val = brown_corpus_texts.humor_cfd[word1].freq(word2)
    if word2 in sf_words:
        val = brown_corpus_texts.sf_cfd[word1].freq(word2)

    #if the word we are choosing is the first of a line, favor words that have a lot of following words
    """
    if start_of_line:
        num_next = [(len(brown_corpus_texts.fiction_cfd[x]), x) for x in brown_corpus_texts.fiction_cfd]
        sorted_next = sorted(num_next)
        for pair in sorted_next:
            if pair[1] == word2:
                val = pair[0]
    """



    return val

def heuristic(haiku, word1, word2, search, start_of_line):
    """combines all heuristics
    string, string -> int"""
    val_1 = distance_heuristic(word1, word2, search)
    val_2 = continuation_heuristic(haiku, word1, word2, search, start_of_line)
    return val_1*.2+val_2*.8