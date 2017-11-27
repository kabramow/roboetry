import constants
import probability_table
import pickle

# myProbabilityTable = probability_table.ProbabilityTable("../haiku_corpus_files/tagged_poems_mancor.txt")
# max_count = 0
# max_word_prob = None
# for word_prob in myProbabilityTable.word_probabilities:
#     # print("Current word is " + word_prob.word + " count is " + str(word_prob.word_count))
#     if word_prob.word_count > max_count:
#         max_count = word_prob.word_count
#         max_word_prob = word_prob
#
# for following in max_word_prob.following_words:
#     print(following)
# print(constants.FAKE_NEW_LINE)
# print(constants.PROBABILITY_TABLE.word_probabilities[12].word)
# print(constants.PROBABILITY_TABLE.word_probabilities[13].word)


# An arbitrary collection of objects supported by pickle.
# data = probability_table.ProbabilityTable("../haiku_corpus_files/tagged_poems_clean.txt")
#
# with open('../haiku_corpus_files/prob.pickle', 'wb') as f:
#     # Pickle the 'data' dictionary using the highest protocol available.
#     pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
#
# data = None
# with open('../haiku_corpus_files/prob.pickle', 'rb') as f:
#     # The protocol version used is detected automatically, so we do not
#     # have to specify it.
#     data = pickle.load(f)


print(constants.PROBABILITY_TABLE.word_probabilities[0].prob_dict)
print(constants.PROBABILITY_TABLE.word_probabilities[2].prob_dict)