# Spelling Bee Project

# imports
import random
from SB_GUI import graphics
import string
import textwrap
import sys
import os

def resource_path(file):
    """Retrieves relative file path so bundled app can find data files"""
    base_path = getattr(
        sys, '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, file)

# get paths for textfiles
words_path = resource_path("words.txt")
good_combos_path = resource_path("Good-Letter-combos.txt")

# open words.txt file for global use
words_list_file = open(words_path, "r")

# define global variables
words_dictionary = []
for word in words_list_file:
    words_dictionary.append(word.lower()[:-1])

letters = [char for char in string.ascii_lowercase]

# window creation
def create_window():
    def clear_fields():
        """function to reset the gui (called when new puzzle is input)"""
        window.show_message("")
        window.clear_word_list()
        window.clear_solutions()
        window.clear_wordbox()
        window.clear_wordcount()
        window.clear_points()
        window.clear_solution_wordcount()
        window.clear_solution_points()
        window.reset_progressbar()
        window.reset_rank()

    def find_words(valid_letters):
        """Takes in 7 unique letters and returns possible words that can be 
        made by combining those words. Also returns a list of pangrams"""
        # redundancy to ensure list input and lowercase chars
        valid_letters = [char.lower() for char in valid_letters]
        invalid_letters = [a for a in letters if a not in valid_letters]
        # center letter will always be the first letter in valid_letters list
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

    def check_word(s):
        """Evaluates words entered in the word entry field and displays 
        words/info, updates score/wordcount/guessed words list, and steps the 
        progressbar"""
        valid_letters = window.get_honeycomb_letters()
        user_word = window.get_field("    Enter Word: ").lower()
        guessed_words = window.get_guessed_words()
        valid_words, pangrams = find_words(valid_letters)
        total_words, total_points = calc_available_word_points(
            valid_words, pangrams)
        # print("entered word: ", user_word)
        # print("words already entered: ", guessed_words)
        # if user guesses an already guessed word:
        if user_word in guessed_words:
            window.show_message(
                f"You have already entered the word '{user_word}'!", "Red")
        # if user guesses a pangram:
        elif user_word in pangrams:
            window.show_message(
                f"Congrats! '{user_word}' is a pangram!", "Gold")
            window.addto_wordbox(user_word, "Gold")
            guessed_words.append(user_word)
            word_points = calc_word_points(user_word, 2)
            window.add_wordcount()
            window.add_points(word_points)
            window.step_progressbar(word_points, total_points)
        # if user guesses a valid, non-pangram word
        elif user_word in valid_words:
            window.show_message(
                f"Entered word '{user_word}' is accepted!", "Green")
            window.addto_wordbox(user_word, "White")
            guessed_words.append(user_word)
            word_points = calc_word_points(user_word, 1)
            window.add_wordcount()
            window.add_points(word_points)
            window.step_progressbar(word_points, total_points)
        else:
            window.show_message(
                f"The word '{user_word}' is not accepted", "Red")

        ranks = ["Beginner", "Good Start", "Moving Up", "Good",
                 "Solid", "Nice", "Great", "Amazing", "Genius"]
        rank_pct_rqrd = [0, 0.01685, 0.04, 0.06, 0.12, 0.2, 0.32, 0.40, 0.56]

        rank_pct_dict = {k: v for k, v in zip(rank_pct_rqrd, ranks)}
        user_points = window.get_points()
        # print("user points: ", user_points)
        for pct in rank_pct_dict:
            if user_points / total_points >= pct:
                window.set_rank(rank_pct_dict[pct])

    def calc_word_points(word, multiplier):
        if len(word) <= 3:
            return 0
        elif len(word) == 4:
            return 1 * multiplier
        elif len(word) >= 5:
            return len(word) * multiplier

    def puzzle_solution(s):
        """Retrieves valid words and pangrams made by the honeycomb letters, 
        then displays them in the solutions textbox with appropriate text 
        color"""
        window.show_message("")
        valid_letters = window.get_honeycomb_letters()
        valid_words, pangrams = find_words(valid_letters)
        for word in valid_words:
            if word in pangrams:
                window.addto_solutions(word, "Gold")
            else:
                window.addto_solutions(word, "White")
        total_words, total_points = calc_available_word_points(
            valid_words, pangrams)
        window.set_solution_wordcount(total_words)
        window.set_solution_points(total_points)

    def calc_available_word_points(valid_words, pangrams):
        """Takes in list of available words and pangrams and returns the number of """
        total_words = len(valid_words)
        total_points = 0
        for word in valid_words:
            if word in pangrams:
                # pangrams worth double the word length
                total_points += 2 * len(word)
            elif len(word) == 4:
                # 4-letter words worth 1 point
                total_points += 1
            elif len(word) >= 5:
                # 5 or > length non-pangram words worth their length
                total_points += len(word)
        return total_words, total_points

    def random_puzzle_pregenerated(s):
        """Selects a random 7-letter combination from the 
        Good-Letter-Combos.txt, which contains 1500 pregenerated 'good' letter 
        combinations. Selected combos are then shuffled to increase variety"""
        with open(good_combos_path, "r") as infile:
            line = next(infile)
            for id, lne in enumerate(infile, 2):
                if random.randrange(id):
                    continue
                line = lne.strip("\n")
            valid_letters = []
            for char in line:
                valid_letters.append(char)
            # randomly shuffle the combo
            random.shuffle(valid_letters)
            # reset gui
            clear_fields()
            # add letters to the honercomb
            window.set_honeycomb_letters(valid_letters)
            

    def input_valid_letters(s):
        """Use entry field to get honeycomb letters... clears gui and adds 
        letters to honeycomb. Input must be 7 characters."""
        user_letters = window.get_field("Custom Puzzle: ").lower()
        if len(user_letters) != 7:
            window.show_message("Please enter 7 characters", "Red")
        else:
            valid_letters = [char.upper() for char in user_letters]
            window.set_honeycomb_letters(valid_letters)
            clear_fields()

    def shuffle_letters(s):
        """Shuffles the current honeycomb letters... keeps the center letter"""
        window.show_message("")
        valid_letters = window.get_honeycomb_letters()
        center_letter = valid_letters[0]
        valid_letters.remove(center_letter)
        random.shuffle(valid_letters)
        valid_letters = [center_letter] + valid_letters
        window.set_honeycomb_letters(valid_letters)

    # create graphics object
    window = graphics()

    # text for the info textbox:
    window.addto_readmebox(
        "This game is a recreation of the New York Times' Spelling Bee game.\n\n")
    paragraph1 = """To begin, press the 'Generate Random Puzzle' button or enter your own letters in the 'Custom Puzzle' field. If you are entering a custom puzzle, be sure to submit exactly 7 unique letters. Pressing the 'Generate Random Puzzle' button will select a combination of letters that will guarantee at least 1 pangram (a word that uses all 7 letters at least once)."""
    paragraph2 = """The objective of the game is to make as many words out of the given letters as you can. Words can use any of the letters any number of times, but must include the center letter. Words must be 4 letters or longer."""
    paragraph3 = """Each 4-letter word guessed is worth 1 point. Words with 5 or more letters will give you points equal to the number of letters. Pangrams are worth points equal to double their word length. As words are entered, the progress bar will adjust incrementally according to the amount of points each word is worth."""
    paragraph4 = """There are 9 ranks you can achieve in each game, starting with 'Beginner' and ending with 'Genius'."""
    paragraph5 = """If you are having trouble finding new words, try pressing the 'Shuffle Letters' button to move the letters in the hexagon around. Click the 'Solve Puzzle' button to see all possible solutions and total number of words/points available. Enter a custom puzzle or press the 'Generate Random Puzzle' button to start over."""
    paragraph6 = """It's also important to note that the word bank for this game is not perfect or identical to the one used by the NYT. There are some words that should be removed and others that should be added."""
    # use TextWrapper for cleaner text wrapping
    wrapper = textwrap.TextWrapper(width=47)
    for text in [paragraph1, paragraph2, paragraph3, paragraph4, paragraph5, paragraph6]:
        line_list = wrapper.wrap(text=text)
        for line in line_list:
            line += "\n"
            window.addto_readmebox(line)
        window.addto_readmebox("\n")

    window.add_field("Custom Puzzle: ", input_valid_letters)
    window.add_field("    Enter Word: ", check_word)
    window.create_button("Generate Random Puzzle", random_puzzle_pregenerated)
    window.create_button("Shuffle Letters", shuffle_letters)
    window.create_button("Solve Puzzle", puzzle_solution)

    window.event_loop()

create_window()

words_list_file.close()

# With pyinstaller, used the following line to generate bundled app (app works on my mac without an Apple developer licence):
# pyinstaller --clean --onefile --windowed --icon=Spelling-Bee-Icon.icns --add-data="words.txt:." --add-data="Good-Letter-Combos.txt:." --add-data="/Users/zanemazorbrown/opt/anaconda3/lib/python3.8/site-packages/customtkinter:customtkinter/" NYT-Spelling-Bee-Project.py

