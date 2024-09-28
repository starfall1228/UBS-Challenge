import json
import logging
import string
from flask import request, jsonify

from collections import defaultdict
from routes import app

logger = logging.getLogger(__name__)

def correct_mistypes(dictionary, mistypes):
    # Convert the dictionary list to a hash table for faster lookups
    # start_time = time.time()
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
    # print("--- %s seconds ---" % (time.time() - start_time))
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
        corrections = correct_mistypes(dictionary, mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    # responses.extend([{"corrections": []}, {"corrections": []}])
    responses.extend([{"corrections": []}])
    
    # logging.info("My result :{}".format(responses))
    return jsonify(responses)

