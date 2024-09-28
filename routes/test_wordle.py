import json
import logging

from flask import request

# from routes import app

logger = logging.getLogger(__name__)

# Function to read word list from a file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    return words

# Load the word list from the text file
WORD_LIST = load_word_list('nyt-answers.txt')
# WORD_LIST = ["slate", "lucky", "maser", "gapes", "wages"]

def filter_words(guess_history, evaluation_history):
    filtered_words = WORD_LIST
    for guess, evaluation in zip(guess_history, evaluation_history):
        new_filtered_words = []
        for word in filtered_words:
            match = True
            for i, (g, e) in enumerate(zip(guess, evaluation)):
                if e == 'X' and word[i] != g:
                    match = False
                    break
                elif e == '-' and word[i] == g:
                    match = False
                    break
                elif e == '?' and (word[i] == g or g not in word):
                    match = False
                    break
            if match:
                new_filtered_words.append(word)
        filtered_words = new_filtered_words
    return filtered_words

# @app.route('/wordle-game', methods=['POST'])
def wordle():
    with open("input_file.json", 'r') as file:
        data = json.load(file)

    # data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))

    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])

    filtered_words = filter_words(guess_history, evaluation_history)

    if filtered_words:
        next_guess = filtered_words[0]
    else:
        next_guess = "arose"

    # logging.info("My result :{}".format(result))
    # return json.dumps(result)

    print(next_guess)
    # logging.info("Next guess: {}".format(next_guess))
    # return json.dumps({"guess": next_guess})


if __name__ == "__main__":
    wordle()
