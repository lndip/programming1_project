"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
StudentId: 150482439
Firstname Lastname: Ngoc Diep Luong
Email: diep.luong@tuni.fi

PROGRAM BEHAVIOUR
- The program is a hangman game in which users enter their guesses through a
virtual keyboard. In each round, the user can choose a level before starting
the game. After the "New Game" button is pressed, the virtual keyboard is
activated. A letter is only chosen once in a round; after being chosen, the button
of that letter is disabled. After finishing a round, the keyboard is disabled.
The user now has 2 options: restarting by choosing a level and pressing "New
Game" or quitting the game by pressing "Quit Game". The user can also start a new
round with the wanted level whenever they want.

- Source of images and audio used in the game:
+ The pictures used in the program are my drawings.
+ The sound played after the user wins or loses a round are downloaded from Mixkit
(website: "https://mixkit.co/"). The original audio names from Mixkit are "Video game win"
and "Retro arcade lose".

NOTE: The sound from the game can only be played if the program is running on
Windows. The module used to play the audio winsound is a built-in module for
Python on Windows. If you run the program on Mac or other operating systems,
please comment out line 33, 178-184, 258, 275. The program then will no longer
have the feature of playing sound after the user wins or loses a round.
"""

# Import the modules and libraries
import random
from tkinter import *
from winsound import *

class Userinterface:
    def __init__(self):
        '''
        Initialize the attributes of the class
        '''
        self.__mainwindow = Tk()
        self.__mainwindow.title("Hangman GUI")
        self.__mainwindow["background"] = 'white'

        # Create the set of words used in the game
        # The words are divided into levels
        self.__word_dict = {
            "Easy": ["VIETNAM", "APPLE", "ORANGE", "EASY", "FINLAND", "BEACH",\
                     "PENCIL", "ERASER", "RULER", "MOUSE", "CHARGER", "WINTER",\
                     "SUMMER", "SPRING", "AUTUMN", "LANTERN", "NOTEBOOK", "BOOTS",\
                     "BOTTLE", "HOODIE", "REEK", "lAPTOP", "CLARION", "POCKET",\
                     "SKATING", "SKIING", "TRAM", "TRAIN", "INTEGRATE", "LIGHTER",\
                     "SCISSORS", "PACKAGE", "LITERATURE", "LITERAL", "BAG", "TOOTHBRUSH",\
                     "TOOTHPASTE", "PERFUME", "BRACE"],

            "Intermediate": ["CALCULATOR", "EVALUATE", "ELEVATOR", "ESCALATE",\
                             "ROUTER", "ENGAGE", "HEADPHONE", "DICTIONARY",\
                             "AMBULANCE", "BACKPACK", "DUVET", "FLAMINGO", "REPUBLIC",\
                             "CUSTODY", "WARRANTY", "EVOLUTIONARY", "MANDATE",\
                             "PUNITIVE", "PRIMITIVE", "LIMITATION", "SITUATION", "OBVIOUS",\
                             "OBLIVIOUS", "INTIMIDATE", "INTERMEDIATE", "IMMEDIATE",\
                             "INTIMATE"],

            "Hard": ["RUCKSACK", "ELUCIDATE", "MANSLAUGHTER", "GENOCIDE", "CONSPIRACY",\
                     "CONSPICUOUS", "PERMUTATION", "DELINEATE", "RHYTHM", "RHETORIC",\
                     "PERPETUATE", "IMPREGNABLE", "CONDESCEND", "ALIENATE", "AGGRAVATE",\
                     "DISDAIN", "REPUGNANT", "RECALIBRATE", "EVANESCE", "SUPPLANT",\
                     "SUBORDINATE","SEGREGATE", "STULTIFY", "SUPERSEDE", "AMBIVALENT",\
                     "SOVEREIGNTY", ""]
        }

        # Create the set of the photos in the hangman game
        self.__images = [PhotoImage(file="img-11.gif"), PhotoImage(file="img-10.gif"),\
                         PhotoImage(file="img-09.gif"), PhotoImage(file="img-08.gif"),\
                         PhotoImage(file="img-07.gif"), PhotoImage(file="img-06.gif"),\
                         PhotoImage(file="img-05.gif"), PhotoImage(file="img-04.gif"),\
                         PhotoImage(file="img-03.gif"), PhotoImage(file="img-02.gif"),\
                         PhotoImage(file="img-01.gif")]
        self.__images_label = Label(self.__mainwindow, image=self.__images[10],borderwidth=0)
        self.__images_label.grid(row=0, rowspan=2, column=0, columnspan=5)

        # Initiate the number of guesses
        # The exact number will be assigned when user press "New Game" button
        self.__no_of_guesses = None

        # Create components used to display the word to user
        self.__word = None
        self.__word_with_space = None

        self.__word_display = StringVar(self.__mainwindow)
        self.__word_display_label = Label(self.__mainwindow, textvariable=self.__word_display)
        self.__word_display_label.grid(row=0, column=5, columnspan=4)
        self.__word_display_label["background"] = 'white'

        # Create the Option Menu for the word's level
        self.word_level_label = Label(self.__mainwindow, text="CHOOSE A LEVEL    ")
        self.word_level_label.grid(sticky="e", row=2,column=0, columnspan=2)
        self.word_level_label["background"] = 'white'

        self.__word_levels = list(self.__word_dict.keys())
        self.__word_level_option = StringVar(self.__mainwindow)
        self.__word_level_option.set(self.__word_levels[0])
        self.__word_level_menu = OptionMenu(self.__mainwindow, self.__word_level_option,
                                            *self.__word_levels)
        self.__word_level_menu.grid(sticky="w", row=2,column=2, columnspan=2)
        self.__word_level_menu.config(width=11)

        # Crete the Announcement Label for the game
        self.__announcement_label = Label(self.__mainwindow, height=2,\
                                          text="Choose a level and click \"New Game\" to start")
        self.__announcement_label.grid(row=1, column=5, columnspan=4)
        self.__announcement_label["background"] = 'white'

        # Create the keyboard for the game
        # The buttons in the keyboard is created by for loop and stored in
        # dictionary self.__keyboard
        # The state of the keyboard before user press "New Game" button is off
        self.__keyboard = {}
        self.__alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","N",\
                    "M","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        n = 0
        for letter in self.__alphabet:
            self.__keyboard[letter] = Button(self.__mainwindow, text=letter,
                                             command=lambda letter=letter: self.guess(letter),
                                             width=8, height=2)
            self.__keyboard[letter].grid(row=(n//9)+3,column=n%9)
            n += 1
        self.set_keyboard_state("Off")

        # Create New Game button
        self.__new_game_button = Button(self.__mainwindow, text="New game", command=self.new_game)
        self.__new_game_button.grid(row=2,column=4,columnspan=3)

        # Create the Quit button
        self.__quit_button = Button(self.__mainwindow, text="Quit game", command=self.quit)
        self.__quit_button.grid(row=2, column=7, columnspan=2)

    def start(self):
        """
        Starts the program
        """
        self.__mainwindow.mainloop()

    def quit(self):
        '''
        Quit the program
        '''
        self.__mainwindow.destroy()

    def set_image(self,image):
        '''
        Set the image corresponding to user's state
        :param image: The image to be set
        :return: None
        '''
        self.__images_label.configure(image=image)

    def set_announcement(self, announcement):
        '''
        Set the announcement which conveys the program's state to the user
        :param announcement: The announcement to be set
        :return: None
        '''
        self.__announcement_label.configure(text=announcement)

    def set_keyboard_state(self,state):
        '''
        Set the state for the keyboard. There are 2 states: "On" and "Off"
        :param state: The state set for the keyboard
        :return: None
        '''
        if state == "Off":
            for letter in self.__alphabet:
                self.__keyboard[letter]["state"] = DISABLED
        elif state == "On":
            for letter in self.__alphabet:
                self.__keyboard[letter]["state"] = NORMAL

    def play_audio(self, audio):
        '''
        Play the input audio file
        :param audio: The name of the audio file (must be WAV file)
        :return: None
        '''
        PlaySound(audio, SND_FILENAME)

    def get_word(self):
        '''
        Get the word for the new round according to the selected level
        :return: None
        '''
        # Get the selected level
        selected_level = self.__word_level_option.get()
        # Randomly take a word in the level chosen by the user
        self.__word = random.choice(self.__word_dict[selected_level])
        # Put space between the letters of the word
        self.__word_with_space = "    ".join(self.__word)

    def new_game(self):
        '''
        Initiate the conditions for the user to start a new round
        :return: None
        '''
        # Set the blank image
        self.set_image(self.__images[10])
        # Set the number of guesses as 10
        self.__no_of_guesses = 10
        # Activate the keyboard
        self.set_keyboard_state("On")
        # Get the word for the new round
        self.get_word()
        # Display the dash for each letter in the word to the user
        self.__word_display.set("    ".join("_" * len(self.__word)))
        # The announcement states the number of guesses
        self.set_announcement("Number of guesses: " + str(self.__no_of_guesses))

    def replace_letter(self, letter):
        '''
        Replace the dash with the letter if the letter is in the word
        :param letter: The guessed letter
        :return: True if the dash is successfully replaced
        '''
        if letter in self.__word:
            # Create a list containing letters in self.__word_display for the replacing step
            temp_word_display = list(self.__word_display.get())

            # Loop over the letters, replace and update the word display on screen to users
            for i in range(len(self.__word_with_space)):
                if self.__word_with_space[i] == letter:
                    temp_word_display[i] = letter
                self.__word_display.set("".join(temp_word_display))
            return True
        return False

    def guess(self, letter):
        '''
        Guess whether a letter is in a word
        - If the letter is in the word, replace the dash with that letter
        in the displayed word to user; congratulate the user if the word is guessed
        - If the letter is not in the word, reduce the number of guesses;
        announce GAME OVER if the number of guesses = 0
        :param letter: The guessed letter
        :return: None
        '''
        # Disable the button for the letter after it is guessed
        self.__keyboard[letter]["state"] = DISABLED

        if self.replace_letter(letter):
            # Update the number of guesses to the user
            self.set_announcement("Number of guesses: " + str(self.__no_of_guesses))

            # If the user get the word right:
            if self.__word_display.get() == self.__word_with_space:
                # Disable the keyboard
                self.set_keyboard_state("Off")
                # Congratulate the user
                self.set_announcement("CONGRATS \n click \"New Game\" to play next round")
                # Play the congratulation audio
                self.play_audio("win-audio.wav")

        else:
            # Update the number of guesses to the user
            self.__no_of_guesses -= 1
            self.set_announcement("Number of guesses: " + str(self.__no_of_guesses))

            # Update the image corresponding to the user's state after a wrong guess
            self.set_image(self.__images[self.__no_of_guesses])

            # If the user get the word wrong:
            if self.__no_of_guesses == 0:
                # Disable the keyboard
                self.set_keyboard_state("Off")
                # Announce that the user lost
                self.set_announcement("GAME OVER \n click \"New Game\" to restart")
                # Play game losing audio
                self.play_audio("lose-audio.wav")

def main():
    ui = Userinterface()
    ui.start()

if __name__ == "__main__":
    main()