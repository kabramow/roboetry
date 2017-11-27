class FollowingWord(object):
    def __init__(self, word, word_count=1):
        self.word = word
        # word count here means number of times word occurred after previous word
        self.word_count = word_count
        # pos of proceeding word as key to dictionary
        # content of dictionary is a sub dictionary
        # with parts of speech as keys and number of occurrences as content
        self.prob_dict = {}

    def __str__(self):
        return "< " + self.word + ", " + str(self.word_count) + ", " + str(self.prob_dict) + " >"

    # check if current pos is in prob dictionary
    def update_prob_dict(self, current_part_of_speech, next_part_of_speech):
        if current_part_of_speech in self.prob_dict:
            # if it is check if next pos is in prob dictionary
            sub_dict = self.prob_dict[current_part_of_speech]
            if next_part_of_speech in sub_dict:
                sub_dict[next_part_of_speech] += 1
            else:
                sub_dict[next_part_of_speech] = 1
        else:
            self.prob_dict[current_part_of_speech] = {}
            self.prob_dict[current_part_of_speech][next_part_of_speech] = 1

    def probability_following_word(self, total_count_current_word):
        return (self.word_count*1.0)/total_count_current_word
