# Defines the 'graphics' class used to generste the GUI for the Spelling Bee game

# imports
import customtkinter as ctk
import tkinter as tk
import math

hex_letter_font = ("Helvetica Neue", -40, "bold")
word_list_font = ("Helvetica Neue", -16, "normal")

window_width = 1000
window_height = 400

# Partially adapted from the work of Eric Roberts and Jed Rembold
class graphics:
    def __init__(self):
        def render_hex(x_start, y_start, color):
            """Generates hexagons at specified x,y coordinates with specified 
            fill color"""
            hex_coords = []
            for point in range(6):
                x = x_start + 40 * math.cos(math.radians(180 - point * 60))
                y = y_start - 40 * math.sin(math.radians(180 - point * 60))
                hex_coords += [x, y]
            self.window.create_polygon(*hex_coords, width=1, fill=color)
            return self.window.create_text(x_start, y_start, text="", font=hex_letter_font, fill="Black")

        def honeycomb():
            """Generates 7 hexagons in a honeycomb pattern - center hex is 
            gold, the others a white. Creates empty text fields in each hexagon 
            which can be edited later"""
            x_start = 160
            y_start = window_height / 2
            self.hex_letters = [render_hex(x_start, y_start, "Gold")]
            for hexagon in range(6):
                x = x_start + 76 * math.cos(math.radians(30 + 60 * hexagon))
                y = y_start - 76 * math.sin(math.radians(30 + 60 * hexagon))
                self.hex_letters.append(render_hex(x, y, "White"))

        def bottom_text():
            """Places empty text field (to be edited later) at the bottom of 
            the screen for flashing messages"""
            self.message = self.window.create_text(
                320, 395, text="", anchor=ctk.SW, font=word_list_font)

        def ranking_text():
            """Places ranking text in the top right side of the window"""
            self.game_ranking = self.window.create_text(
                640, 48, text="Current Rank: -", anchor=ctk.SW, font=word_list_font)

        def wordcount_text():
            """Places player wordcount text below the player guessed words 
            textbox"""
            self.player_wordcount_text = self.window.create_text(
                320, 345, text="Word Count:", anchor=ctk.SW, font=word_list_font)

        def score_text():
            """Places player score text below the player guessed words 
            textbox"""
            self.player_score_text = self.window.create_text(
                320, 365, text="Points:", anchor=ctk.SW, font=word_list_font)

        def solution_wordcount_text():
            """Places total attainable wordcount text below the solutions list
            textbox"""
            self.solution_player_wordcount_text = self.window.create_text(
                480, 345, text="", anchor=ctk.SW, font=word_list_font)

        def solution_score_text():
            """Places total attainable points text below the solutions list
            textbox"""
            self.solution_player_score_text = self.window.create_text(
                480, 365, text="", anchor=ctk.SW, font=word_list_font)

        def delete_window():
            """Close function to configure window protocol"""
            self._ctk.destroy()

        # Build window:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self._ctk = ctk.CTk()
        self._ctk.title("Spelling Bee")
        self._ctk.protocol("WM_DELETE_WINDOW", delete_window)
        # prevent window from being resized
        self._ctk.resizable(width=False, height=False)

        # define reused class variables:
        self.window = tk.Canvas(
            self._ctk, width=window_width, height=window_height)
        self.window.pack()
        self.controls = ctk.CTkFrame(self._ctk)
        self.interactors = ctk.CTkFrame(self.controls)
        self.fields = {}
        self.wordlist = []
        self.solution_list = []
        self.words_guessed = []
        self.letters = ""
        self.player_word_count = 0
        self.player_score = 0

        # WORDS TEXT BOX
        self.wordbox = ctk.CTkTextbox(
            self.window, width=120, height=235, activate_scrollbars=True)
        self.wordbox.configure(state="disabled")
        self.wordbox.place(anchor=ctk.SW, x=320, y=320)
        self.wordbox.tag_config("Gold", foreground="Gold")
        self.wordbox.tag_config("White", foreground="White")

        # SOLUTIONS TEXT BOX
        self.solutionsbox = ctk.CTkTextbox(
            self.window, width=120, height=235, activate_scrollbars=True)
        self.solutionsbox.configure(state="disabled")
        self.solutionsbox.place(anchor=ctk.SW, x=480, y=320)
        self.solutionsbox.tag_config("Gold", foreground="Gold")
        self.solutionsbox.tag_config("White", foreground="White")

        # READ ME TEXT
        self.readmebox = ctk.CTkTextbox(
            self.window, width=320, height=235, activate_scrollbars=True)
        self.readmebox.configure(state="disabled")
        self.readmebox.place(anchor=ctk.SW, x=640, y=320)
        self.readmebox.tag_config("White", foreground="White")

        # PROGRESS BAR
        self.progressbar = ctk.CTkProgressBar(self.window)
        self.progressbar.configure(width=280, height=20)
        self.progressbar.place(anchor=ctk.SW, x=320, y=50)
        self.progressbar.set(0)

        # Generate honeycomb and place text fields
        honeycomb()
        bottom_text()
        ranking_text()
        wordcount_text()
        score_text()
        solution_wordcount_text()
        solution_score_text()

    def step_progressbar(self, word_points, total_points):
        """Steps progressbar by a given words point value relative to the 
        amount of total points in the puzzle"""
        current_value = self.progressbar.get()
        # enable the following line to see exact value of prgrsbar in console
        # print(f"Current progressbar value = {current_value}")
        step_value = (word_points / total_points) + current_value
        # enable following line to view prgrsbar value of last guessed word
        # print(f"Value after stepping = {step_value}")
        self.progressbar.set(step_value)

    def reset_progressbar(self):
        """Resets the progressbar value to 0"""
        self.progressbar.set(0)

    def reset_rank(self):
        """Resets the player rank text in the top right side of the window"""
        self.window.itemconfigure(self.game_ranking, text="Current Rank: ")

    def addto_readmebox(self, text, color="White"):
        """Adds text to the wide textbox on the right side of the window"""
        # textbox must be configured to normal before inserting text, then 
        # closed to prevent users from editing
        self.readmebox.configure(state="normal")
        self.readmebox.insert(ctk.END, text, color)
        self.readmebox.configure(state="disabled")

    def addto_wordbox(self, word, color):
        """Adds text to the player guessed words textbox closest to the 
        honeycomb"""
        self.wordbox.configure(state="normal")
        word += "\n"
        self.wordbox.insert(ctk.END, word, color)
        self.wordbox.configure(state="disabled")

    def clear_wordbox(self):
        """Clears all player-guessed words in the textbox closest to the 
        honeycomb"""
        self.wordbox.configure(state="normal")
        self.wordbox.delete("0.0", "end")
        self.wordbox.configure(state="disabled")

    def addto_solutions(self, word, color):
        """Adds text to the solution words textbox in the middle"""
        self.solutionsbox.configure(state="normal")
        word += "\n"
        self.solutionsbox.insert(ctk.END, word, color)
        self.solutionsbox.configure(state="disabled")

    def clear_solutions(self):
        """Clears all text in the solution words textbox, if there is any"""
        self.solutionsbox.configure(state="normal")
        self.solutionsbox.delete("0.0", "end")
        self.solutionsbox.configure(state="disabled")

    def create_button(self, name, callback):
        """Create a ctk button on the command strip at the bottom of the screen"""
        def button_action():
            callback(name)
        padding = ctk.CTkFrame(self.interactors)
        padding.pack(side=ctk.LEFT, padx=6)
        border = ctk.CTkFrame(padding)
        border.pack()
        button = ctk.CTkButton(
            border, text=name, command=button_action)
        button.pack()

    def add_field(self, name, callback, nchars=120):
        """Add an entry field on the command strip at the bottom of the screen"""
        def enter_action(text):
            callback(textvar.get())
            entry.delete(0, ctk.END)

        padding = ctk.CTkFrame(self.interactors)
        padding.pack(side=ctk.LEFT)
        label = ctk.CTkLabel(padding, text=" " + name)
        label.pack()
        padding = ctk.CTkFrame(self.interactors)
        padding.pack(side=ctk.LEFT)
        border = ctk.CTkFrame(padding)
        border.pack()
        textvar = ctk.StringVar()
        entry = ctk.CTkEntry(border, width=nchars,
                             textvariable=textvar)
        entry.bind("<Return>", enter_action)
        entry.pack()
        self.fields[name] = textvar

    def get_field(self, name):
        """Gets value from specified entry field"""
        return self.fields[name].get()

    def get_guessed_words(self):
        """Gets list of valid words guessed by user"""
        return self.words_guessed

    def clear_wordcount(self):
        """Resets player wordcount/wordcount text for current game"""
        self.window.itemconfigure(
            self.player_wordcount_text, text="Word Count:")
        self.player_word_count = 0

    def add_wordcount(self):
        """Increments player wordcount by one if invoked"""
        self.player_word_count += 1
        msg = f"Word Count:{self.player_word_count:>6}"
        self.window.itemconfigure(
            self.player_wordcount_text, text=msg)

    def get_points(self):
        """Gets player score (int) value for current game"""
        return int(self.player_score)

    def clear_points(self):
        """Resets player score/score text for current game"""
        self.window.itemconfigure(self.player_score_text, text="Points:")
        self.player_score = 0

    def add_points(self, points):
        """Adds specified value to player points for the current game. Updates 
        Player points text."""
        self.player_score += points
        msg = f"Points:{self.player_score:>16}"
        self.window.itemconfigure(self.player_score_text, text=msg)

    def set_solution_wordcount(self, wordcount):
        """Edits solutions wordcount text to display a wordcount under the 
        solution words textbox"""
        self.solution_wordcount = wordcount
        msg = f"Word Count:{self.solution_wordcount:>6}"
        self.window.itemconfigure(
            self.solution_player_wordcount_text, text=msg)

    def clear_solution_wordcount(self):
        """Removes solutions wordcount text under the solutions words textbox"""
        self.window.itemconfigure(self.solution_player_wordcount_text, text="")
        self.solution_wordcount = 0

    def set_solution_points(self, points):
        """Edits solutions points text to display a score under the solution 
        words textbox"""
        self.solution_points = points
        msg = f"Points:{self.solution_points:>16}"
        self.window.itemconfigure(self.solution_player_score_text, text=msg)

    def clear_solution_points(self):
        """Removes solutions points text under the solution words textbox"""
        self.window.itemconfigure(self.solution_player_score_text, text="")
        self.solution_points = 0

    def event_loop(self):
        """Starts main loop"""
        self.interactors.pack()
        self.controls.pack(expand=True, fill=ctk.X)
        self._ctk.mainloop()

    def set_honeycomb_letters(self, letters):
        """Adds letters to the hexagons rendered on screen"""
        self.letters = letters
        for letter in range(len(letters)):
            self.window.itemconfigure(
                self.hex_letters[letter], text=self.letters[letter])

    def get_honeycomb_letters(self):
        """Returns a list of current letters placed in the honeycomb. The first 
        letter will always be from the center hexagon"""
        return self.letters

    def clear_word_list(self):
        for word in self.wordlist:
            self.window.delete(word)
        self.words_guessed = []
        self.wordlist.clear()
        self.word_lst_x = 300
        self.word_lst_y = 30

    def clear_solution_list(self):
        for word in self.solution_list:
            self.window.delete(word)
        self.solution_list.clear()
        self.solution_x = 500
        self.solution_y = 30

    def show_message(self, msg, color="White"):
        self.window.itemconfigure(self.message, text=msg, fill=color)

    def set_rank(self, rank, color="White"):
        msg = f"Current Rank:{rank:>11}"
        self.window.itemconfigure(self.game_ranking, text=msg, fill=color)
