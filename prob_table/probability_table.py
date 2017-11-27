import nltk
from prob_table import pos_probability as pp
from prob_table import word_probability as wp
from prob_table import following_word


# An Object that represents a series of probabilities for various
# grammar/word/part of speech occurrences
class ProbabilityTable(object):
    def __init__(self, file_name="../haiku_corpus_files/tagged_poems_mancor.txt"):
        # a list of POSProbability
        # See pos_probability.py for more information
        self.pos_probabilities = []
        # a list of WordProbability
        # see word_probability for more information
        self.word_probabilities = []
        # tracks how many poems are in the training corpus
        self.poem_count = 0
        # tracks how many words are in the training corpus
        self.word_count = 0
        # a dictionary of what words start a poem and how often those words do start a poem
        self.starting_words = {}
        # a dictionary of what parts of speech start a poem and how often those pos do begin a poem
        self.starting_pos = {}

        file = open(file_name, 'r')
        text = file.read()
        file.close()
        lines = text.split("\n")
        for line in lines:
            # line does not represent corrected line which contains ->
            if line.find("->") == -1:
                self.poem_count += 1
                # split into word/part_of_speech tags
                tagged_tokens = [nltk.tag.str2tuple(w) for w in line.split(" ")]
                self.word_count += len(tagged_tokens)
                for i in range(0, len(tagged_tokens)-2):
                    current_word = tagged_tokens[i][0]
                    current_part_of_speech = tagged_tokens[i][1]
                    next_word = tagged_tokens[i+1][0]
                    next_part_of_speech = tagged_tokens[i+1][1]

                    # add to starting words and starting parts of speech if first word in poem
                    if i == 0:
                        if current_word in self.starting_words:
                            self.starting_words[current_word] = self.starting_words[current_word] + 1
                        else:
                            self.starting_words[current_word] = 1

                        if current_part_of_speech in self.starting_pos:
                            self.starting_pos[current_part_of_speech] = self.starting_pos[current_part_of_speech] + 1
                        else:
                            self.starting_pos[current_part_of_speech] = 1

                    # check if word is already in word_probabilities
                    existing_word_prob = self.find_word(current_word)
                    if existing_word_prob is not None:
                        existing_word_prob.word_count = existing_word_prob.word_count + 1
                        wp.WordProbability.add_new_instance(existing_word_prob, current_part_of_speech,
                                                            next_word, next_part_of_speech)
                    else:
                        new_word_prob = wp.WordProbability(current_word, 1)
                        new_word_prob.prob_dict[current_part_of_speech] = 1
                        new_following_word = following_word.FollowingWord(next_word, 1)
                        # creates a dictionary to represent value for key
                        new_following_word.prob_dict[current_part_of_speech] = {}
                        new_following_word.prob_dict[current_part_of_speech][next_part_of_speech] = 1
                        self.word_probabilities.append(new_word_prob)

                    # check if part of speech is already in pos_probabilities
                    existing_part_of_speech_prob = self.find_part_of_speech(current_part_of_speech)
                    if existing_part_of_speech_prob is not None:
                        existing_part_of_speech_prob.pos_tag_count = existing_part_of_speech_prob.pos_tag_count + 1
                        pp.POSProbability.update_prob_dictionary(existing_part_of_speech_prob, next_part_of_speech)
                    else:
                        new_part_of_speech_prob = pp.POSProbability(current_part_of_speech, 1)
                        new_part_of_speech_prob.prob_dict[next_part_of_speech] = 1
                        self.pos_probabilities.append(new_part_of_speech_prob)

    # Returns word probability if word is in word_probabilities
    def find_word(self, word):
        for word_prob in self.word_probabilities:
            if word_prob.word == word:
                return word_prob
        return None

    # Returns part of speech probability if word is in pos_probabilities
    def find_part_of_speech(self, part_of_speech):
        for pos in self.pos_probabilities:
            if pos.pos_tag == part_of_speech:
                return pos
        return None
