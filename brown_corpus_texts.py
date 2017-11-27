import constants
import nltk
from nltk.corpus import brown
from nltk.util import bigrams

"""Pulling training texts. In each corpus, association rules are used to pull words that follow one another
and the frequency (i.e. probability(word2|word1)) is computed"""

# Text: Boroff: Jewish Teenage Culture
lore_corpus = brown.words(categories="lore")
lore_lc_corp = [w.lower() for w in lore_corpus]
lore_common_bigrams = [(x, y) for (x, y) in bigrams(lore_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
lore_cfd = nltk.ConditionalFreqDist(lore_common_bigrams)

# Text: W.E.B. Du Bois: Worlds of Color
fiction_corpus = brown.words(categories="fiction")
fiction_lc_corp = [w.lower() for w in fiction_corpus]
fiction_common_bigrams = [(x, y) for (x, y) in bigrams(fiction_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
fiction_cfd = nltk.ConditionalFreqDist(fiction_common_bigrams)

# Text: Callaghan: A Passion in Rome
romance_corpus = brown.words(categories="romance")
romance_lc_corp = [w.lower() for w in romance_corpus]
romance_common_bigrams = [(x, y) for (x, y) in bigrams(romance_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
romance_cfd = nltk.ConditionalFreqDist(romance_common_bigrams)

# Text: Hitchens: Footsteps in the Night
mystery_corpus = brown.words(categories="mystery")
mystery_lc_corp = [w.lower() for w in fiction_corpus]
mystery_common_bigrams = [(x, y) for (x, y) in bigrams(mystery_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
mystery_cfd = nltk.ConditionalFreqDist(mystery_common_bigrams)

#Text: Field: Rattlesnake Ridge
adventure_corpus = brown.words(categories="adventure")
adventure_lc_corp = [w.lower() for w in adventure_corpus]
adventure_common_bigrams = [(x, y) for (x, y) in bigrams(adventure_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
adventure_cfd = nltk.ConditionalFreqDist(adventure_common_bigrams)

# Text: Thurber: The Future, If Any, of Comedy
humor_corpus = brown.words(categories="humor")
humor_lc_corp = [w.lower() for w in humor_corpus]
humor_common_bigrams = [(x, y) for (x, y) in bigrams(humor_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
humor_cfd = nltk.ConditionalFreqDist(humor_common_bigrams)

# Text: Heinlein: Stranger in a Strange Land
sf_corpus = brown.words(categories="science_fiction")
sf_lc_corp = [w.lower() for w in sf_corpus]
sf_common_bigrams = [(x, y) for (x, y) in bigrams(sf_lc_corp)
                       if x in constants.PRONUNCIATION_DICT and y in constants.PRONUNCIATION_DICT]
sf_cfd = nltk.ConditionalFreqDist(sf_common_bigrams)
