import constants
import probability_table

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


print(constants.PROBABILITY_TABLE.word_probabilities[12].word)
print(constants.PROBABILITY_TABLE.word_probabilities[13].word)
