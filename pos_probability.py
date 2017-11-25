class POSProbability(object):
    def __init__(self, pos_tag, pos_tag_count, prob_dict):
        self.pos_tag = pos_tag
        self.pos_tag_count = pos_tag_count
        # a dictionary with key pos of following word
        # and content number of times that pos occurs
        self.prob_dict = prob_dict
