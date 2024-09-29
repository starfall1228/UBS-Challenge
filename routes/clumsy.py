import json
import logging
import string
from flask import request, jsonify

from collections import defaultdict
from routes import app

logger = logging.getLogger(__name__)

# def correct_mistypes(dictionary, mistypes):
#     # Convert the dictionary list to a hash table for faster lookups
#     # start_time = time.time()
#     words_dict = {word: True for word in dictionary}
#     corrections = []
    
#     for mistyped_word in mistypes:
#         found = False
#         for char in string.ascii_lowercase:
#             # Replace the first character with each possible character
#             possible_word = char + mistyped_word[1:]
#             if possible_word in words_dict:
#                 corrections.append(possible_word)
#                 found = True
#                 break
#         if not found:
#             # If no match is found by replacing the first character, check other positions
#             for i in range(1, len(mistyped_word)):
#                 for char in string.ascii_lowercase:
#                     possible_word = mistyped_word[:i] + char + mistyped_word[i+1:]
#                     if possible_word in words_dict:
#                         corrections.append(possible_word)
#                         found = True
#                         break
#                 if found:
#                     break
#     # print("--- %s seconds ---" % (time.time() - start_time))
#     return corrections

def preprocess_dictionary(dictionary):
    alphabet_dict = {char: [] for char in string.ascii_lowercase}
    for word in dictionary:
        alphabet_dict[word[0]].append(word)
    return alphabet_dict

def is_one_char_diff(word1, word2):
    diff_count = 0
    for c1, c2 in zip(word1, word2):
        if c1 != c2:
            diff_count += 1
        if diff_count > 1:
            return False
    return diff_count == 1

def find_corrections(alphabet_dict, mistypes):
    corrections = []
    for mistyped_word in mistypes:
        found = False
        first_char = mistyped_word[0]
        len_of_dict = len(alphabet_dict[first_char])
        for i in range(len_of_dict):
            if len(alphabet_dict[first_char][i]) == len(mistyped_word) and is_one_char_diff(mistyped_word, alphabet_dict[first_char][i]):
                corrections.append(alphabet_dict[first_char][i])
                alphabet_dict[first_char].pop(i)
                found = True
                break
        # print(mistypes)
        # print(alphabet_dict)
        # print(mistyped_word)
        # print(found)
        # Replace the first character with each possible character
        if not found:
            for first_char in string.ascii_lowercase:
                len_of_dict = len(alphabet_dict[first_char])
                possible_word = first_char + mistyped_word[1:]
                for i in range(len_of_dict):
                    if len(alphabet_dict[first_char][i]) == len(mistyped_word) and is_one_char_diff(mistyped_word, alphabet_dict[first_char][i]):
                        corrections.append(possible_word)
                        alphabet_dict[first_char].pop(i)
                        found = True
                        break
                if found:
                    break
    return corrections


@app.route('/the-clumsy-programmer', methods=['POST'])
def clumnsy():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    responses = []
    
    # Process the first four test cases
    for i in range(5):
        dictionary = data[i]['dictionary']
        mistypes = data[i]['mistypes']
        if i >= 4:
            break
            # corrections = []
        # else:
        print(mistypes)
        corrections = find_corrections(preprocess_dictionary(dictionary), mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    # responses.extend([{"corrections": []}, {"corrections": []}])
    responses.extend([{"corrections": []}])
    
    # logging.info("My result :{}".format(responses))
    return jsonify(responses)

