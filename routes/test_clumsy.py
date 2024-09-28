
import time

def correct_mistypes(dictionary, mistypes):
    start_time = time.time()
    
    # Convert the dictionary list to a hash table for faster lookups
    # words_dict = {word: True for word in dictionary}
    words_dict = dictionary
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
    
    end_time = time.time()
    print(f"Time taken for correction: {end_time - start_time:.6f} seconds")
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
