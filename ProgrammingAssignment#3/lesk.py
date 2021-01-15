# Paarth Lakhani
# u0936913

import sys
import re
from collections import OrderedDict

test_sentences_data_file = sys.argv[1]
sense_definitions_data_file = sys.argv[2]
stopwords_data_file = sys.argv[3]

test_sentences_data = open('./data/' + test_sentences_data_file, 'r')
sense_definitions_data = open('./data/' + sense_definitions_data_file, 'r')
stopwords_data_file = open('./data/' + stopwords_data_file, 'r')
test_sentences = test_sentences_data.readlines()
sense_definitions = sense_definitions_data.readlines()
stopwords = stopwords_data_file.readlines()
stopwords_strip_new_lines = []
output_file_name = test_sentences_data_file + ".lesk"
output_file_data = open('./' + output_file_name, 'w')


for stopword in stopwords:
    stopwords_strip_new_lines.append(stopword.strip("\n").lower())


senses_dict = {}
for sense_definition in sense_definitions:
    sense_definition_words = sense_definition.split()
    sense_words = set()
    for sense_definition_word_index in range(1, len(sense_definition_words)):
        if (sense_definition_words[sense_definition_word_index]) not in stopwords_strip_new_lines:
            if re.search("^.*[A-Za-z]+.*$", sense_definition_words[sense_definition_word_index]):
                sense_words.add(sense_definition_words[sense_definition_word_index].lower())
    senses_dict[sense_definition_words[0]] = sense_words


def compute_overlap(signature, context, word):
    overlap_score = 0
    for context_word in context:
        if context_word in signature:
            if context_word is not word:
                overlap_score = overlap_score + 1
    return overlap_score


def simplified_lesk(test_sentence):
    sense_ranking = {}
    context = set()
    word = re.findall("<occurrence>(.+?)</>", test_sentence)  # Check this later
    sentence_words = test_sentence.split()
    for sentence_word in sentence_words:
        if sentence_word not in stopwords_strip_new_lines:
            if re.search("^.*[A-Za-z]+.*$", sentence_word):
                if "<occurrence>" not in sentence_word:
                    context.add(sentence_word.lower())
    for sense, signature in senses_dict.items():
        overlap = compute_overlap(signature, context, word)
        sense_ranking[sense] = overlap
    return sense_ranking


sense_rankings = ""
final_output_write = ""
for test_sentence in test_sentences:
    sense_ranking = simplified_lesk(test_sentence)
    sense_ranking = OrderedDict(sorted(sense_ranking.items(), key=lambda t: t[0]))
    sense_ranking = sorted(sense_ranking.items(), key=lambda x: x[1], reverse=True)
    sense_ranking_list = []
    for sense_overlays in sense_ranking:
        sense_ranking_list.append(sense_overlays[0] + "(" + str(sense_overlays[1]) + ")")
    final_output_write = final_output_write + " ".join(sense_ranking_list) + "\n"
final_output_write = final_output_write.strip("\n")
output_file_data.write(final_output_write)

output_file_data.close()
