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
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import word_node
import word_probability as wp
import pos_probability as pp
import following_word as fw



def poem_searcher(haiku, search_space, p_search_lines):
    """Returns a 5-7-5 Haiku based off of heuristics
    String, list -> list"""
    syll = 17
    last_word_score = 0
    frontier = PriorityQueue()
    pass_through = 0
    num_syllables = 5 #starting number for first line
    search_lines = p_search_lines
    start_of_line = False #tells us if the word we are picking is the first in a line
    poem = [[], [], []]
    explored = []
    updated_search_space = []

    stopWords = set(stopwords.words('english')) #stop words = unimportant words -> a, the, etc.
    #filtering out stop words
    for w in search_space:
        if w not in stopWords:
            updated_search_space.append(w)

    #saving words as objects so we can assign h,f,g values to them
    j=0
    nodes = []
    for word in updated_search_space:
        nodes.append(word_node.Word(word))

    #Choosing first word -> picked based from first part of text, favor words that have
    #a lot of potential continuations
    first_word_search_space = updated_search_space[:int(len(updated_search_space) / 5)]
    num_next = [(len(haiku.cfd[x]), x) for x in haiku.cfd]
    sorted_next = sorted(num_next) #list of continuation words
    first_word = sorted_next[-1][1] #this will be the word with the most continuation words
    first_word = word_node.Word(first_word)

    #making sure the word is useable/a good word
    i=1
    while first_word.word not in first_word_search_space or first_word.word not in constants.PRONUNCIATION_DICT:
        first_word = sorted_next[-i][1]
        i+=1
        first_word = word_node.Word(first_word)

    # update the number of syllables left we have to work with
    syll_remaining = num_syllables - syllabifier.get_syllables(first_word.word)
    syll += syllabifier.get_syllables(first_word.word)

    # append our chosen word to the corresponding line of our poem
    poem[pass_through].append(first_word.word)

    # add our first word to the frontier
    first_word.h = heuristic(haiku, first_word.word, first_word.word, search_lines, start_of_line, poem)
    first_word.g = syll*-1 #how close we are to the goal = how many syllables we have left
    first_word.f = first_word.h+first_word.g
    frontier.put((first_word.f, first_word))

    finished = False

    while frontier:
        frontier.get() #grab first word
        explored.append(first_word)
        # checking if we've finished all 3 lines of the haiku
        if pass_through == 2 and syll_remaining == 0:
            finished = True
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

        index_of_current_word = updated_search_space.index(first_word.word)
        #We need to reference individual words, but also whole lines to know what position
        #we are at in the html output. Rather than continually changing between data structures
        #(i.e. between a regular list and a nested list), we keep track of both cocurrently
        #so that we may rather reference which ever one we need at the moment
        updated_search_space = updated_search_space[index_of_current_word+1:]
        nodes = nodes[index_of_current_word + 1:]
        search_lines = update_search_lines(search_lines, first_word.word)
        frontier = PriorityQueue()
        neighbors = get_neighbors_list(first_word.word, nodes)
        for neighbor in neighbors:
            if neighbor.word in constants.PRONUNCIATION_DICT and syllabifier.get_syllables(neighbor.word) <= syll_remaining\
                    and neighbor.word!=first_word.word:
                # neighbors = all possible words, frontier = usable words, with heuristic values
                if not (is_present(frontier.queue,neighbor) or neighbor in explored):
                    neighbor.h = heuristic(haiku, first_word.word, neighbor.word, search_lines,start_of_line, poem)
                    neighbor.g = first_word.g + syll*-1  # how many syllables we have left - i.e. how close we are to
                    # the goal (but we are working all in negatives with PQ)
                    neighbor.f = neighbor.g + neighbor.h
                    frontier.put((neighbor.f, neighbor))
                else:
                    neighborH = heuristic(haiku, first_word.word, neighbor.word, search_lines,start_of_line, poem)
                    neighborG = first_word.g + syll*-1
                    neighborF = neighborG + neighborH
                    if neighborF < neighbor.f:
                        neighbor.f = neighborf
                        frontier.put((neighbor.f,neighbor))
                    if neighbor in explored:
                        explored.remove(neighbor)
                    if neighbor not in frontier:
                        frontier.append(neighbor)

        if frontier.queue:
            # grab first word in Priority Queue - i.e. WORD WITH LOWEST HEURISTIC
            first_word = sorted(list(frontier.queue))[0][1]
        else:
            break
        syll_remaining -= syllabifier.get_syllables(first_word.word)
        syll += syllabifier.get_syllables(first_word)
        poem[pass_through].append(first_word.word)

    if finished == False:
        print("Syllable requirements not met.")
        return poem

    return poem

def is_present(queue, neighbor):
    """checks if a Word object is present in a queue

    Queue, Word -> Boolean"""
    in_frontier = False
    for word_pair in queue:
        if word_pair[1] == neighbor.word:
            in_frontier = True
            current_score = word_pair[0]
            break
        else:
            in_frontier = False
    return in_frontier


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
    neighbors = []
    neighbors = list[0:int(len(list)/3)]

    return neighbors



def distance_between_words(word1, word2, search_lines):
    """calculates 'euclidean distance' of two words in html output
    and uses common normalization of 1/(1+d(p1,p2) to convert
    to measure of similarity
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

    val = math.sqrt(math.pow((xpos2 - xpos1), 2) + math.pow((ypos2 - ypos1),2))
    return 1/(1+ val)*-1 #multiplying to normalize values in comparison to other measures


def continuation_probability(haiku, word1, word2, start_of_line):
    """using training corpus, returns value symbolizing how likely word2 is
     to follow word1, based on word continuations in corpus texts

     Haiku object, string, string, boolean -> int"""
    val = 1 #place holder value

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
                print("HERE ", pair[1], pair[0])
    """
    if val != 1:
        return val*-1
    else:
        return val

def semantic_similarity_to_poem(word2, poem):
    """Measures the similarity between a word and the poem that has
    been created so far. This is to ensure the poem has a cohesive theme.
    For technical details, see docString of semantic_similarity_to_previous_word()

    String, nested list -> int"""
    sum = 0
    total = 0
    val = 0
    if wordnet.synsets(word2):
        w2syn = wordnet.synsets(word2)[0].name()
        w2 = wordnet.synset(w2syn)
        #print(w2)
        for line in poem:
            for word in line:
                if word2 == word:
                   return 1
                if wordnet.synsets(word):
                    w1syn = wordnet.synsets(word)[0].name()
                    w1 = wordnet.synset(w1syn)
                    total+=1
                    if w1.wup_similarity(w2):
                        sum+=(w1.wup_similarity(w2))
    if sum != 0:
        val = (sum/total)
    if val == 1:
        return 1
    return val*-1

def semantic_similarity_to_previous_word(word1, word2):
    """Measures the semantic similarity between words
    synsets = list of synonyms
    synset = string containing word and part of speech
    wup_similarity = similarity measure in decimals

    String, string -> int"""
    val = 1
    if wordnet.synsets(word2) and wordnet.synsets(word1):
        w2syn = wordnet.synsets(word2)[0].name()
        w2 = wordnet.synset(w2syn)
        w1syn = wordnet.synsets(word1)[0].name()
        w1 = wordnet.synset(w1syn)
        if w1.wup_similarity(w2):
            val = (w1.wup_similarity(w2))
            #print(word1, word2, w1.wup_similarity(w2))
    if val == 1:
        return 1
    return val*-1

def grammar_heuristic(word1, word2):
    # if first word is in training corpus return probability that second word comes after it
    # if second word in training corpus data
    prob_table = constants.PROBABILITY_TABLE
    word_prob = prob_table.find_word(word1)
    if word_prob is not None:
        following_word = wp.WordProbability.contains_following_word(word_prob, word2)
        if following_word is not None:
            return fw.FollowingWord.probability_following_word(following_word, word_prob.word_count)*-100
        else:
            # find part of speech of word2
            word2_pos = nltk.pos_tag(word2)[0][1]
            return wp.WordProbability.part_of_speech_prob(word_prob, word2_pos)*-20
    else:
        word1_pos = nltk.pos_tag(word1)[0][1]
        word2_pos = nltk.pos_tag(word2)[0][1]
        pos_prob = prob_table.find_part_of_speech(word1_pos)
        if pos_prob is not None:
            return pp.POSProbability.following_pos_probability(pos_prob, word2_pos)*-10
        else:
            return 1


def heuristic(haiku, word1, word2, search, start_of_line, poem):
    """combines all similarity values into one heuristic value
    NOTE: each value is a negative, wherein the lowest value represents
    the closest match (i.e. -5 is better than 0). Since a Priority Queue is used,
    this means the lowest negative will be chosen first.
    string, string -> int"""
    distance = distance_between_words(word1, word2, search)
    continuation = continuation_probability(haiku, word1, word2, start_of_line)
    sem_poem = semantic_similarity_to_previous_word(word1, word2)
    sem_word = semantic_similarity_to_poem(word2, poem)
    grammar = grammar_heuristic(word1, word2)
    #topic_sim = similarity_to_topic(word2, poem)
    liklihood_of_traliing_word = distance + continuation + sem_poem + sem_word + grammar
    return liklihood_of_traliing_word