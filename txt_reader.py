import random


def get_random_selection(file_name):
    num_lines = 20
    f = open(file_name, 'r')
    text = f.read()
    f.close()

    lines = text.split('\n')

    start_point = random.randint(0, len(lines)-100)
    updated_message = ""
    line_count = 0
    for i in range(start_point, start_point + 100):

        if line_count < num_lines:
            if lines[i] != "":
                updated_message += lines[i]
                updated_message += " \n "
                line_count += 1
        else:
            return updated_message


def get_up_to_20_random_words(string):
    ret_list = []
    lines = string.split('\n')
    num_lines = len(lines)
    if num_lines > 20:
        random_lines = []
        for i in range(0, 20):
            new_int = random.randint(0, num_lines-1)
            if new_int not in random_lines:
                random_lines.append(new_int)

        random_lines.sort()
        print(random_lines)
        for pos in random_lines:
            words = lines[pos].split(" ")
            if len(words) > 0:
                word_pos = random.randint(0, len(words)-1)
                new_word = words[word_pos]
                if new_word != '':
                    ret_list.append(new_word)
    elif num_lines > 0:
        for line in lines:
            words = line.split(" ")
            if len(words) > 0:
                word_pos = random.randint(0, len(words))
                ret_list.append(words[word_pos])

    return ret_list


def get_title(file_name):
    f = open(file_name, 'r')
    text = f.read()
    f.close()

    lines = text.split('\n')
    first_line = lines[0]
    title = first_line.replace("The Project Gutenberg EBook of ", "")
    "American Fairy Tales, by L. Frank Baum"
    title = title.replace(", by ", " </i>by ")
    title = "<i>" + title

    return title
