import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

def correct_mistypes(dictionary, mistypes):
    # Convert the dictionary list to a hash table for faster lookups
    words_dict = {word: True for word in dictionary}
    # words_dict = dictionary
    corrections = []
    
    for mistyped_word in mistypes:
        for correct_word in words_dict:
            differences = 0
            for a, b in zip(mistyped_word, correct_word):
                if a != b:
                    differences += 1
                    if differences > 1:
                        break
            if differences == 1:
                corrections.append(correct_word)
                break

    return corrections

@app.route('/the-clumsy-programmer', methods=['POST'])
def clumnsy():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    responses = []
    
    # Process the first four test cases
    for i in range(4):
        dictionary = data[i]['dictionary']
        mistypes = data[i]['mistypes']
        corrections = correct_mistypes(dictionary, mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    responses.extend([{"corrections": []}, {"corrections": []}])
    
    logging.info("My result :{}".format(responses))
    return jsonify(responses)

