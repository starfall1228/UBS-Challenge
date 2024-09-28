import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

'''
Solve the Wordle
wordle

Instructions
Wordle is a popular online word game where players have to guess a 5-letter word in 6 attempts. After each guess, the game provides feedback on which letters are correct, which are in the word but in the wrong position, and which are not in the word at all.

Your task is to write a program that can programmatically solve Wordle puzzles. The program should take the feedback from previous guess(es) as input and then suggest the next best word to guess. The program should do the opening guess as well since we won't provide any starter guess.

Expose a POST endpoint /wordle-game for verification

Expected request mime-type: application/json Expected response mime-type: application/json

Game Rule
Each evaluation consists of 10 games. Each game is a single Wordle game with same rules with the popular wordle game, i.e. max 6 guesses. We will run through loops to check if the program can solve the game within 6 guesses.

However, for each nth guess, the nth character will be masked and no feedback will be provided. The final (6th) guess will have the full feedback, not masked. If you guess correctly, then the feedback will not be masekd.

Expected Input
string guess
{
    "guess": "lucky"
}
Expected Output
Every test case will have the following format:

list<string> guessHistory
list<string> evaluationHistory
{
   "guessHistory": ["slate"], 
   "evaluationHistory": ["?-X-X"]
}
Symbols
O (letter O) means it is in correct position (green in real game).
X (letter X) means it include the letter but in wrong position (yellow in real game).
- (dash) means it does not include the letter (gray in real game)
? (Question mark) means the feedback is masked.
Rules/Constraints
Similar to Wordle, at max 6 guesses each game
Examples
Case: Success
Full game sequence:

Request:

{
   "guessHistory": [], 
   "evaluationHistory": []
},
Response

{
    "guess": "slate"
}
Request:

{
   "guessHistory": ["slate"], 
   "evaluationHistory": ["?-X-X"]
},

'''

# Function to read word list from a file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    return words

# Load the word list from the text file
# WORD_LIST = load_word_list('nyt-answers.txt')
WORD_LIST = ["slate", "lucky", "maser", "gapes", "wages"]

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

@app.route('/wordle-game', methods=['POST'])
def wordle():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])

    filtered_words = filter_words(guess_history, evaluation_history)

    if filtered_words:
        next_guess = filtered_words[0]
    else:
        next_guess = "arose"

    # logging.info("My result :{}".format(result))
    # return json.dumps(result)

    logging.info("Next guess: {}".format(next_guess))
    return json.dumps({"guess": next_guess})


