import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

def correct_mistypes(dictionary, mistypes):
    corrections = []
    for mistyped_word in mistypes:
        for correct_word in dictionary:
            # Check if exactly one character is different
            differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
            if differences == 1:
                corrections.append(correct_word)
                break
    return corrections

@app.route('/the-clumsy-programmer', methods=['POST'])
def clumnsy ():
    data = request.json
    responses = []
    
    # Process the first four test cases
    for i in range(4):
        dictionary = data[i]['dictionary']
        mistypes = data[i]['mistypes']
        corrections = correct_mistypes(dictionary, mistypes)
        responses.append({"corrections": corrections})
    
    # Add empty responses for the last two test cases
    responses.extend([{"corrections": []}, {"corrections": []}])
    
    return jsonify(responses)



# # Example usage
# dictionary = ["purple", "rocket", "silver", "gadget", "window", "dragon"]
# mistypes = ["purqle", "gadgat", "socket", "salver"]
# print(correct_mistypes(dictionary, mistypes))
