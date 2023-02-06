#       Selects good combinations of letters for the spelling bee program.
#       Each generated combination of letters will contain at least 20 valid
#       words and at least 1 pangram. The string result will be randomized
#       when called from the main program.

#       Used Google Colab to generate a list of 1500 good combinations.

# imports
import string
import random
import codecs

# Use codecs to handle words with characters not supported in utf-8
words = codecs.open("words.txt", 'r', 'utf-8', errors="replace")
words_dictionary = []
for word in words:
    words_dictionary.append(word.lower()[:-1])


def find_words(valid_letters):
    """Returns lists of valid words and valid pangrams given valid letters"""
    letters = [char for char in string.ascii_lowercase]
    valid_letters = [char.lower() for char in valid_letters]
    invalid_letters = [a for a in letters if a not in valid_letters]
    center_letter = valid_letters[0]
    valid_words = []
    for word in words_dictionary:
        if center_letter in word \
                and len(word) >= 4 \
                and any(a in invalid_letters for a in word) == False \
                and word not in valid_words:
            valid_words.append(word)
    pangrams = []
    for word in valid_words:
        if valid_letters[0] in word \
                and valid_letters[1] in word \
                and valid_letters[2] in word \
                and valid_letters[3] in word \
                and valid_letters[4] in word \
                and valid_letters[5] in word \
                and valid_letters[6] in word:
            pangrams.append(word)
    return valid_words, pangrams

def random_puzzle():
    """Generates sets of 7 unique characters until the set produces at least 20
    words and at least 1 pangram"""
    letters = string.ascii_uppercase
    iter_vari = 0
    while True:
        iter_vari += 1
        valid_letters = random.sample(letters, 7)
        valid_words, pangrams = find_words(valid_letters)
        valid_letters_string = ""
        if len(valid_words) > 20 and len(pangrams) > 0:
            for letter in valid_letters:
                valid_letters_string += letter
            break
        else:
            continue
    print(f"It took {iter_vari} attempts to make these letters")
    print(
        f"There are {len(valid_words)} words available and {len(pangrams)} pangrams")
    return valid_letters_string

# Generate 1500 good letter combos and store in a txt file
with open("Good-Letter-Combos.txt", "w+", newline="") as outfile:
    for i in range(1, 1501):
        good_combo = random_puzzle() + "\n"
        print(f"Item {i} generated")
        outfile.write(good_combo)
