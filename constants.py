from nltk.corpus import cmudict
import pickle

PRONUNCIATION_DICT = cmudict.dict()
FAKE_NEW_LINE = "00thisisnotarealnewline00"
PROBABILITY_TABLE = None
with open('../haiku_corpus_files/data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    PROBABILITY_TABLE = pickle.load(f)
