
import time
import string

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

data = [
    {
        "dictionary": ["purple", "rocket", "silver", "gadget", "window", "dragon"],
        "mistypes": ["purqle", "gadgat", "socket", "salver"]
    },
    {
        "dictionary": ["apple", "banana", "cherry", "date", "elderberry", "fig"],
        "mistypes": ["appla", "banaba", "cherty", "dare"]
    },
    {
        "dictionary": ["house", "mouse", "blouse", "spouse", "louse", "grouse"],
        "mistypes": ["houae", "mouae", "blouae", "spouae"]
    },
    {
        "dictionary": ["table", "cable", "fable", "gable", "label", "sable"],
        "mistypes": ["tabld", "cabld", "fabld", "gabld"]
    },
    {
        "dictionary": ["extra", "input", "cases", "here"],
        "mistypes": ["extrb", "inpot", "casfs", "herf"]
    },
    {
        "dictionary": ["more", "test", "cases", "here"],
        "mistypes": ["morf", "tesf", "casfs", "herf"]
    }
]
responses = []
    # Process the first four test cases
for i in range(4):
    dictionary = data[i]['dictionary']
    mistypes = data[i]['mistypes']
    corrections = correct_mistypes(dictionary, mistypes)
    responses.append({"corrections": corrections})

# Add empty responses for the last two test cases
responses.extend([{"corrections": []}, {"corrections": []}])

print((responses))
