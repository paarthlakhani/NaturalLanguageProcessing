import sys
import re

train_data_file_name = sys.argv[1]
test_data_file_name = sys.argv[2]
word_ftype = sys.argv[3]
f_type_lists = []

if len(sys.argv) > 4:
    for argv_no in range(4, len(sys.argv)):
        f_type_lists.append(sys.argv[argv_no])

possible_labels = {"O": 0, "B-PER": 1, "I-PER": 2, "B-LOC": 3, "I-LOC": 4, "B-ORG": 5, "I-ORG": 6}


def is_abbreviation(word):
    alphanum_period_regex = "^[a-zA-Z\.]+$"
    if len(word) > 4:
        return "no"
    elif word[len(word) - 1] != ".":
        return "no"
    elif not re.search(alphanum_period_regex, word):
        return "no"
    return "yes"


def is_cap(word):
    if not re.search("^[A-Z]$", word[0]):
        return "no"
    return "yes"


def create_readable_files(filename, f_type_list, possible_labels):
    data_file = open('./Entities/' + filename, 'r')
    readable_output_file_name = filename + ".readable"
    vector_output_file_name = filename + ".vector"
    readable_output_file = open(readable_output_file_name, 'w')
    vector_output_file = open(vector_output_file_name, 'w')

    unique_words = set()
    unique_pos = set()
    printed_new_line = False
    data = data_file.readlines()
    for line in data:
        if line != "\n":
            line = line.strip("\n")
            word_parts = line.split(" ")
            word_parts = [word for word in word_parts if word]
            word_feature = word_parts[2]
            unique_words.add(word_parts[2])
            unique_pos.add(word_parts[1])
            readable_output_file.write("WORD: " + word_feature + "\n")
            pos_feature = "n/a"
            abbr_feature = "n/a"
            cap_feature = "n/a"
            wordcon_feature = "n/a"
            poscon_feature = "n/a"
            if "POS" in f_type_list:
                pos_feature = word_parts[1]
            readable_output_file.write("POS: " + pos_feature + "\n")
            if "ABBR" in f_type_list:
                abbr_feature = is_abbreviation(word_parts[2])
            readable_output_file.write("ABBR: " + abbr_feature + "\n")
            if "CAP" in f_type_list:
                cap_feature = is_cap(word_parts[0])
            readable_output_file.write("CAP: " + cap_feature + "\n")
            readable_output_file.write("WORDCON: " + wordcon_feature + "\n")
            readable_output_file.write("POSCON: " + poscon_feature + "\n")
            printed_new_line = False
            readable_output_file.write("\n")

    features = unique_words | unique_pos
    features.add("ABBR_FEATURE")
    features.add("CAP_FEATURE")
    readable_output_file.close()
    vector_output_file.close()


create_readable_files(train_data_file_name, f_type_lists, possible_labels)
create_readable_files(test_data_file_name, f_type_lists, possible_labels)
