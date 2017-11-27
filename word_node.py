class Word(object):
    """word_node class represents a word"""

    def __init__(self, word, parent = None):
        self.word = word
        self.parent = parent
        self.h = 0
        self.g = 0
        self.f = self.g + self.h

    def __lt__(self, other):
        if self.word < other.word:
            return True