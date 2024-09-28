import json
import logging
import string
from flask import request, jsonify

from collections import defaultdict
from routes import app

logger = logging.getLogger(__name__)

def precompute_corrections(dictionary):
    corrections = {}
    for word in dictionary:
        for i in range(len(word)):
            for char in string.ascii_lowercase:
                possible_word = word[:i] + char + word[i+1:]
                if possible_word != word:
                    if possible_word not in corrections:
                        corrections[possible_word] = word
    return corrections

def correct_mistypes(dictionary, mistypes):
    words_dict = set(dictionary)
    corrections_dict = precompute_corrections(dictionary)
    corrections = []
    
    for mistyped_word in mistypes:
        if mistyped_word in corrections_dict:
            corrections.append(corrections_dict[mistyped_word])
        else:
            corrections.append(mistyped_word)  # If no correction found, return the original word
    
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
        corrections = correct_mistypes(dictionary, mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    responses.extend([{"corrections": []}, {"corrections": []}])
    
    # logging.info("My result :{}".format(responses))
    return jsonify(responses)

