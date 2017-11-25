import nltk
import word_probability as wp
import following_word


class ProbabilityTable(object):
    def __init__(self, file_name="../haiku_corpus_files/tagged_poems_mancor.txt"):
        # a list of POSProbability
        self.pos_probabilities = []
        # a list of WordProbability
        self.word_probabilities = []
        # TODO something to keep track of words that start a poem

        file = open(file_name, 'r')
        text = file.read()
        file.close()
        lines = text.split("\n")
        for line in lines:
            # line does not represent corrected line which contains ->
            if line.find("->") == -1:
                # split into word/part_of_speech tags
                tagged_tokens = [nltk.tag.str2tuple(w) for w in line.split(" ")]
                for i in range(0, len(tagged_tokens)-2):
                    current_word = tagged_tokens[i][0]
                    current_part_of_speech = tagged_tokens[i][1]
                    next_word = tagged_tokens[i+1][0]
                    next_part_of_speech = tagged_tokens[i+1][1]

                    existing_word_prob = self.contains_word(current_word)
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

    # Returns word probability if word is in word_probabilities
    def contains_word(self, word):
        for word_prob in self.word_probabilities:
            if word_prob.word == word:
                return word_prob
        return None

    # Returns part of speech probability if word is in pos_probabilities
    def contains_part_of_speech(self, part_of_speech):
        for word_prob in self.pos_probabilities:
            if word_prob.word is part_of_speech:
                return word_prob
        return None

    def following_probability(self, next_word, next_part_of_speech):
        #TODO
        pass
