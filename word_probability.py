import following_word as fw


class WordProbability(object):
    def __init__(self, word, word_count=1):
        self.word = word
        self.word_count = word_count
        # a dictionary with key pos
        # and content number of times that pos occurs
        self.prob_dict = {}
        # a list of type FollowingWord
        self.following_words = []

    def add_new_instance(self, current_part_of_speech, next_word, next_part_of_speech):
        # add 1 to total instances of word
        self.word_count += 1
        # update prob dictionary
        self.update_prob_dictionary(current_part_of_speech)
        # check if next word is in following words list
        existing_following_word = self.contains_following_word(next_word)
        if existing_following_word is not None:
            existing_following_word.word_count = existing_following_word.word_count + 1
            fw.FollowingWord.update_prob_dict(existing_following_word, current_part_of_speech, next_part_of_speech)
        else:
            new_following_word = fw.FollowingWord(next_word, 1)
            new_following_word.prob_dict[current_part_of_speech] = {}
            new_following_word.prob_dict[current_part_of_speech][next_part_of_speech] = 1
            self.following_words.append(new_following_word)

    def contains_following_word(self, candidate_word):
        for follow_word in self.following_words:
            if follow_word.word == candidate_word:
                return follow_word
        return None

    # If prob dictionary does not contain pos create entry otherwise increment
    def update_prob_dictionary(self, part_of_speech):
        if part_of_speech in self.prob_dict:
            self.prob_dict[part_of_speech] += 1
        else:
            self.prob_dict[part_of_speech] = 1
