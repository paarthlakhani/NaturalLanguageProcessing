# Paarth Lakhani
# u0936913

import re
import sys
from collections import OrderedDict

import numpy as np

train_file_name = sys.argv[1]
test_file_name = sys.argv[2]
stopwords_file_name = sys.argv[3]
context_window_size = sys.argv[4]

train_file = open('./data/' + train_file_name, 'r')
test_file = open('./data/' + test_file_name, 'r')
stopwords_file = open('./data/' + stopwords_file_name, 'r')
train_file_contents = train_file.readlines()
test_file_contents = test_file.readlines()
stopwords = stopwords_file.readlines()
stopwords_strip_new_lines = []
output_file_name = test_file_name + ".distsim"
output_file_data = open('./' + output_file_name, 'w')

for stopword in stopwords:
    stopwords_strip_new_lines.append(stopword.strip("\n").lower())

vocabulary = {}
sense_inventory_dict = {}
for train_sentence in train_file_contents:
    before_target_words = train_sentence.split("<occurrence>")[0].split()
    goldsense = before_target_words.pop(0).split(":")
    sense_inventory_dict[goldsense[1]] = []
    after_target_words = train_sentence.split("</>")[1].split()
    if int(context_window_size) != 0:
        context_window_size_before = int(context_window_size)
        context_window_size_after = int(context_window_size)
    else:
        context_window_size_before = int(len(before_target_words))
        context_window_size_after = int(len(after_target_words))
    for i in range(len(before_target_words) - 1, -1, -1):
        if context_window_size_before > 0:
            if before_target_words[i].lower() in vocabulary:
                vocabulary[before_target_words[i].lower()] = vocabulary[before_target_words[i].lower()] + 1
            else:
                vocabulary[before_target_words[i].lower()] = 1
            context_window_size_before = context_window_size_before - 1
        else:
            break
    for i in range(0, len(after_target_words)):
        if i < context_window_size_after:
            if after_target_words[i].lower() in vocabulary:
                vocabulary[after_target_words[i].lower()] = vocabulary[after_target_words[i].lower()] + 1
            else:
                vocabulary[after_target_words[i].lower()] = 1
        else:
            break

keys_to_remove = set()
for key in vocabulary.keys():
    if key in stopwords_strip_new_lines:
        keys_to_remove.add(key)
        #vocabulary.pop(key, None)
    elif not re.search("^.*[A-Za-z]+.*$", key):
        keys_to_remove.add(key)
        #vocabulary.pop(key, None)
    elif vocabulary[key] == 1:
        keys_to_remove.add(key)
        #vocabulary.pop(key, None)

for key_to_remove in keys_to_remove:
    vocabulary.pop(key_to_remove)

vocabulary_words = vocabulary.keys()

def filter_vocab(word_freq_to_filter):
    for key in word_freq_to_filter.keys():
        if key in stopwords_strip_new_lines:
            word_freq_to_filter.pop(key, None)
        elif not re.search("^.*[A-Za-z]+.*$", key):
            word_freq_to_filter.pop(key, None)
        elif word_freq_to_filter[key] == 1:
            word_freq_to_filter.pop(key, None)
    return word_freq_to_filter

for key in sense_inventory_dict.keys():
    goldsense_key = "GOLDSENSE:" + key
    context_words_with_freq_for_key = {}
    for train_sentence in train_file_contents:
        goldsense_in_train = train_sentence.split()[0]
        if goldsense_key == goldsense_in_train:
            before_target_words = train_sentence.split("<occurrence>")[0].split()
            before_target_words.pop(0).split(":")
            after_target_words = train_sentence.split("</>")[1].split()
            if int(context_window_size) != 0:
                context_window_size_before = int(context_window_size)
                context_window_size_after = int(context_window_size)
            else:
                context_window_size_before = int(len(before_target_words))
                context_window_size_after = int(len(after_target_words))
            for i in range(len(before_target_words) - 1, -1, -1):
                if context_window_size_before > 0:
                    if before_target_words[i].lower() in context_words_with_freq_for_key:
                        context_words_with_freq_for_key[before_target_words[i].lower()] = context_words_with_freq_for_key[before_target_words[i].lower()] + 1
                    else:
                        context_words_with_freq_for_key[before_target_words[i].lower()] = 1
                    context_window_size_before = context_window_size_before - 1
                else:
                    break
            for i in range(0, len(after_target_words)):
                if i < context_window_size_after:
                    if after_target_words[i].lower() in context_words_with_freq_for_key:
                        context_words_with_freq_for_key[after_target_words[i].lower()] = context_words_with_freq_for_key[after_target_words[i].lower()] + 1
                    else:
                        context_words_with_freq_for_key[after_target_words[i].lower()] = 1
                else:
                    break

    signature_vector = [0]*len(vocabulary_words)
    for word in context_words_with_freq_for_key:
        if word in vocabulary_words:
            index = list(vocabulary_words).index(word)
            freq = context_words_with_freq_for_key.get(word)
            signature_vector[index] = freq
    sense_inventory_dict[key] = signature_vector

output_file_data.write("Number of Training Sentences = " + str(len(train_file_contents)) + "\n")
output_file_data.write("Number of Test Sentences = " + str(len(test_file_contents)) + "\n")
output_file_data.write("Number of Gold Senses = " + str(len(sense_inventory_dict.keys())) + "\n")
output_file_data.write("Vocabulary Size = " + str(len(vocabulary_words)) + "\n")
final_cos_similarities = ""
for test_sentence in test_file_contents:
    context_vector = [0] * len(vocabulary_words)
    test_words_dict = {}
    cos_similiarity_dict = {}
    before_target_words = test_sentence.split("<occurrence>")[0].split()
    after_target_words = test_sentence.split("</>")[1].split()
    if int(context_window_size) != 0:
        context_window_size_before = int(context_window_size)
        context_window_size_after = int(context_window_size)
    else:
        context_window_size_before = int(len(before_target_words))
        context_window_size_after = int(len(after_target_words))
    for i in range(len(before_target_words) - 1, -1, -1):
        if context_window_size_before > 0:
            if before_target_words[i].lower() in test_words_dict:
                test_words_dict[before_target_words[i].lower()] = test_words_dict[before_target_words[i].lower()] + 1
            else:
                test_words_dict[before_target_words[i].lower()] = 1
            context_window_size_before = context_window_size_before - 1
        else:
            break
    for i in range(0, len(after_target_words)):
        if i < context_window_size_after:
            if after_target_words[i].lower() in test_words_dict:
                test_words_dict[after_target_words[i].lower()] = test_words_dict[after_target_words[i].lower()] + 1
            else:
                test_words_dict[after_target_words[i].lower()] = 1
        else:
            break
    for test_word in test_words_dict:
        if test_word in vocabulary_words:
            index = list(vocabulary_words).index(test_word)
            freq = test_words_dict.get(test_word)
            context_vector[index] = freq

    for gold_sense, signature_vector in sense_inventory_dict.items():
        normalization = np.linalg.norm(context_vector) * np.linalg.norm(signature_vector)
        cos_similiarity = 0
        if normalization != 0:
            dot_product = np.dot(context_vector, signature_vector)
            cos_similiarity = dot_product/normalization
        cos_similiarity_dict[gold_sense] = cos_similiarity
    sense_ranking = OrderedDict(sorted(cos_similiarity_dict.items(), key=lambda t: t[0]))
    sense_ranking = sorted(cos_similiarity_dict.items(), key=lambda x: x[1], reverse=True)
    sense_ranking_list = []
    for cos_score in sense_ranking:
        sense_ranking_list.append(cos_score[0] + "(" + str('{:.2f}'.format(round(cos_score[1], 2))) + ")")
    final_cos_similarities = final_cos_similarities + " ".join(sense_ranking_list) + "\n"
final_cos_similarities = final_cos_similarities.strip("\n")
output_file_data.write(final_cos_similarities)


output_file_data.close()
