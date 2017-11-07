import txt_to_html, txt_reader

text = txt_reader.get_random_selection("american_fairy_tales_baum.txt")
poem_words = txt_reader.get_up_to_20_random_words(text)

txt_to_html.wrap_string_in_html("huh", poem_words, text)
