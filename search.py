import syllabifier
from queue import PriorityQueue
import random
import math
import constants
import nltk


def poem_searcher(search_space, p_search_lines):
    """Returns a 5-7-5 Haiku based off of heuristics
    String, list -> list"""

    frontier = PriorityQueue()
    line_number = 0
    num_syllables = 5
    search_lines = p_search_lines
    poem = [[], [], []]

    # CODE FOR PICKING START WORD (RANDOM)
    # start word must be towards beginning of text
    first_word_search_space = search_space[:int(len(search_space) / 5)]
    first_word = random.choice(first_word_search_space)
    # update the number of syllables left we have to work with
    syll_remaining = num_syllables - syllabifier.get_syllables(first_word)
    # append our chosen word to the corresponding line of our poem
    poem[line_number].append(first_word)
    # add our first word to the frontier
    # frontier.put((heuristic(first_word, first_word), first_word))
    # print('FIRST SEARCH SPACE IS ', first_word_search_space)
    # print("FIRST WORD IS ", first_word)

    updated_search_space = search_space
    # UPDATING OUR TEXT - the search space will define what is or is not a neighbor of a word
    # index_of_first_word = search_space.index(first_word)
    # print("index is ", index_of_first_word)
    # updated_search_space = search_space[index_of_first_word+1:]
    # print("SECOND SEARCH SPACE IS", updated_search_space)

    finished = False

    while not finished:
        # checking if we've finished all 3 lines of the haiku
        if line_number == 2 and syll_remaining == 0:
            finished = True
            break
        # checking if we're done with the first line: if so, we need to start on a new line with 7 syllables
        elif line_number == 0 and syll_remaining == 0:
            syll_remaining = 7
            line_number = 1
        # checking if we're done with the second line: if so, we need to start on a new line with 5 syllables
        elif line_number == 1 and syll_remaining == 0:
            syll_remaining = 5
            line_number = 2

        index_of_current_word = updated_search_space.index(first_word)
        updated_search_space = updated_search_space[index_of_current_word + 1:]
        search_lines = update_search_lines(search_lines, first_word)

        # debugging - disregard
        # print("NEW WORD IS: ", first_word)
        # print("SEARCH LINES: " , search_lines)
        # print("INDEX IS: ", index_of_current_word)
        # print("NEW SEARCH SPACE ", updated_search_space)
        # print("neighbors are: ", get_neighbors_list(first_word, updated_search_space))
        # print("FRONTIER IS ", frontier.queue)

        # UPDATING THE FRONTIER
        # print("FIRST NEIGHBORS ARE ", get_neighbors_list(first_word, updated_search_space))
        for neighbor in get_neighbors_list(first_word, updated_search_space):
            if neighbor in constants.PRONUNCIATION_DICT and syllabifier.get_syllables(neighbor) <= syll_remaining:
                # neighbors = all possible words, frontier = usable words
                frontier.put((heuristic(first_word, neighbor, search_lines), neighbor))

        if frontier.queue:
            # grab first word in Priority Queue - i.e. WORD WITH LOWEST HEURISTIC
            first_word = sorted(list(frontier.queue))[0][1]

        else:
            break

        # RESET FRONTIER
        frontier = PriorityQueue()
        syll_remaining -= syllabifier.get_syllables(first_word)
        poem[line_number].append(first_word)
        # print(syll_remaining)
        # print(poem)

    if finished is False:
        print("POEM FAILED, TRY AGAIN")
        return poem
        # this will try again with a different random start word - it should work when we have real heuristics
        # right now, it will still pick the same words in succession so continually run forever
        # self.poem_search(search_space, 0)
        # return ""
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
        if index_to_cut is not None:
            break

    return_lines = search_lines[index_to_cut:]
    return_lines[0] = return_lines[0][y_to_cut:]
    return return_lines


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
        row_count1 += 1
        if xpos1 is not None and ypos1 is not None:
            break

    for row in search_lines:
        for word in row:
            if word == word2:
                xpos2 = row_count2
                ypos2 = row.index(word)
                break
        row_count2+=1
        if xpos2 is not None and ypos2 is not None:
            break

    if word1 == word2:
        return 5
    # print("WORD ONE IS ", word1, " ", x pos1, " ", y pos1, " AND WORD TWO IS ", word2, " ", x pos2, " ", y pos2, 
    # " AND THE DISTANCE IS ", val)
    val = math.sqrt(math.pow((xpos2 - xpos1), 2) + math.pow((ypos2 - ypos1),2))
    return val


def get_neighbors_list(word, ls):
    """returns words following given word
    string, list -> list"""
    neighbors = ls[0:int(len(ls)/2)]

    return neighbors


def random_heuristic(word1, word2):
    """Not to be used in final submission, basically disregards articles and
    favors the pattern of short word - long word - short word"""
    val = 0
    if word1 == 'a' or word1 == 'and' or word1 == 'the' or word1 == 's' \
            or word2 == 'a' or word2 == 'and' or word2 == 't' or word2 == 's':
        val = 5
    elif len(word1) > len(word2):
        val = (len(word1) - len(word2)) * -1
    elif len(word2) > len(word1):
        val = syllabifier.get_syllables(word2) * -1 - len(word2)
    else:
        if word1 == word2:
            val = 5
        else:
            val = -5
    return val


def heuristic(word1, word2, search):
    """combines all heuristics
    string, string -> int"""
    val_1 = distance_heuristic(word1, word2, search)
    #sprint("Distance heuristic yields " + str(val_1))
    val_2 = random_heuristic(word1, word2)
    return val_2+val_1
