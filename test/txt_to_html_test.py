import txt_to_html, txt_reader, nltk

text = txt_reader.get_random_selection("american_fairy_tales_baum.txt")
poem_words = txt_reader.get_up_to_20_random_words(text)

txt_to_html.wrap_string_in_html("test2", poem_words, text)

# nltk.download('punkt')
# sentence = """At eight \"o'clock on Thursday morning\"
#  Mr. Arthur couldn't feel very good. And this is another sentence."""
# tokens = nltk.word_tokenize(sentence)
# print(tokens)

txt_to_html.poem_generator(["1","2","3","4"])
