import txt_to_html, nltk


txt_to_html.wrap_string_in_html("test2", "american_fairy_tales_baum.txt")

# nltk.download('punkt')
# sentence = """At eight \"o'clock on Thursday morning\"
#  Mr. Arthur couldn't feel very good. And this is another sentence."""
# tokens = nltk.word_tokenize(sentence)
# print(tokens)

txt_to_html.poem_generator(["1","2","3","4"])
