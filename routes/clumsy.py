import json
import logging
import string
from flask import request, jsonify

from collections import defaultdict
from routes import app

logger = logging.getLogger(__name__)

# def group_words_by_first_character(words):
#     grouped_dict = defaultdict(list)
#     for word in words:
#         grouped_dict[word[0]].append(word)
#     return grouped_dict

# def correct_mistypes(dictionary, mistypes):
#     # Group the dictionary words by their first character
#     grouped_dict = group_words_by_first_character(dictionary)
#     corrections = []
    
#     for mistyped_word in mistypes:
#         found = False
#         # Check the group of words with the same first character
#         for correct_word in grouped_dict[mistyped_word[0]]:
#             differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
#             if differences == 1:
#                 corrections.append(correct_word)
#                 found = True
#                 break
        
#         if not found:
#             # If no match is found, try replacing the first character
#             for char in string.ascii_lowercase:
#                 if char == mistyped_word[0]:
#                     continue
#                 for correct_word in grouped_dict[char]:
#                     differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
#                     if differences == 1:
#                         corrections.append(correct_word)
#                         found = True
#                         break
#                 if found:
#                     break
#     return corrections

def correct_mistypes(dictionary, mistypes):
    # Convert the dictionary list to a hash table for faster lookups
    words_dict = {word: True for word in dictionary}
    corrections = []
    
    for mistyped_word in mistypes:
        found = False
        for char in string.ascii_lowercase:
            # Replace the first character with each possible character
            possible_word = char + mistyped_word[1:]
            if possible_word in words_dict:
                corrections.append(possible_word)
                found = True
                break
        if not found:
            # If no match is found by replacing the first character, check other positions
            for i in range(1, len(mistyped_word)):
                for char in string.ascii_lowercase:
                    possible_word = mistyped_word[:i] + char + mistyped_word[i+1:]
                    if possible_word in words_dict:
                        corrections.append(possible_word)
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
    for i in range(6):
        dictionary = data[i]['dictionary']
        mistypes = data[i]['mistypes']
        if i >= 4:
            break
            # corrections = []
        # else:
        print(dictionary)
        corrections = correct_mistypes(dictionary, mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    responses.extend([{"corrections": []}, {"corrections": []}])
    
    # logging.info("My result :{}".format(responses))
    return jsonify(responses)

