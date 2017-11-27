import txt_to_html

files_to_read = [("secondtreatise", "second_treatise.txt"), ("americanfairytales", "american_fairy_tales_baum.txt"),
                 ("prideandprejudice", "pride_and_prejudice.txt")]

for file_tup in files_to_read:
    txt_to_html.wrap_string_in_html(file_tup[0], file_tup[1])


