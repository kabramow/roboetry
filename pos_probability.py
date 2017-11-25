class POSProbability(object):
    def __init__(self, pos_tag, pos_tag_count):
        self.pos_tag = pos_tag
        self.pos_tag_count = pos_tag_count
        # a dictionary with key pos of following word
        # and content number of times that pos occurs
        self.prob_dict = {}

    def update_prob_dictionary(self, next_part_of_speech):
        # update prob dictionary
        if next_part_of_speech in self.prob_dict:
            self.prob_dict[next_part_of_speech] = self.prob_dict[next_part_of_speech] + 1
        else:
            self.prob_dict[next_part_of_speech] = 1

    def following_pos_probability(self, following_pos):
        if following_pos in self.prob_dict:
            return (self.prob_dict[following_pos]*1.0)/self.pos_tag_count
        else:
            return 0
