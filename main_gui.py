# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 14:59:04 2019

@author: Clint Mooney
"""

from load_data import get_data

import random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, DictProperty
from kivy.graphics import Line, Color, Rectangle

# Defines HangmanGUI:
class HangmanGUI(BoxLayout):
    alphabet = StringProperty('abcdefghijklmnopqrstuvwxyz')
    word_list = ListProperty()
    word_to_guess = StringProperty()
    guesses = DictProperty()
    word_blanked = StringProperty()
    
    def __init__(self, word_choices, **kwargs):
        super().__init__(**kwargs)
        self.word_list = word_choices
        Clock.schedule_once(lambda dt: self.gen_word(), .5)
    
    def gen_word(self):
        self.word_to_guess = random.choice(self.word_list)
        self.word_blanked = self.word_to_guess
        self.init_guesses()
        self.draw_man()
        self.gen_input()
        for i in range(len(self.word_to_guess)):
            if self.word_to_guess[i].isalpha():
                self.word_blanked  = self.word_blanked.replace(self.word_to_guess[i], '_')
        self.disp_word()
    
    def draw_man(self):
        count = 0
        for letter in self.guesses.values():
            if not letter and letter != None:
                count += 1
        self.ids['drawing_area'].draw(count)
        if count >= 6:
            self.continue_prompt(False)
    
    def init_guesses(self):
        for letter in self.alphabet:
            self.guesses[letter] = None
    
    def gen_input(self):
        self.ids['remaining_guesses'].clear_widgets()
        wrong_text = ""
        right_text = ""
        for letter in self.alphabet:
            if self.guesses[letter] == None:
                this_button = Button(text=letter)
                this_button.size_hint = (.3, .11)
                this_button.bind(on_press=self.process_guess)
                self.ids['remaining_guesses'].add_widget(this_button)
            elif self.guesses[letter] == True:
                if len(right_text) != 0:
                    right_text += ', '
                right_text += letter
            elif self.guesses[letter] == False:
                if len(wrong_text) != 0:
                    wrong_text += ', '
                wrong_text += letter
        self.ids['wrong_text'].text = wrong_text
        self.ids['right_text'].text = right_text
    
    def process_guess(self, button):
        letter = button.text
        for i in range(len(self.word_to_guess)):
            if self.word_to_guess[i] == letter:
                self.word_blanked = self.word_blanked[:i] + letter + self.word_blanked[i + 1:]
                self.guesses[letter] = True
                break
            else:
                self.guesses[letter] = False
        if '_' not in self.word_blanked:
            self.continue_prompt(True)
        else:
            self.disp_word()
            self.gen_input()
            self.draw_man()
    
    def disp_word(self):
        self.ids['word_site'].text = self.word_blanked
    
    # Function called after end of game to ask player if they would like to continue:
    def continue_prompt(self, match_won):
        text_to_display = ""
        if match_won:
            text_to_display = "Congratulations! You won by figuring out the word \"{}!\" Would you like to continue playing?"
        else:
            text_to_display = "Sorry, the word was \"{}.\" Would you like to continue playing?"
        text_to_display = text_to_display.format(self.word_to_guess)
        self.ids['remaining_guesses'].clear_widgets()
        
        self.ids['word_site'].font_size = '12sp'
        self.ids['word_site'].text = text_to_display
        self.ids['word_site'].size_hint = (None, .25)
        continueUI = GridLayout(cols=2)
        contButton = Button(size_hint=(.05,.05), text="Continue?")
        contButton.bind(on_press=self.continue_game)
        continueUI.add_widget(contButton)
        quitButton = Button(size_hint=(.05,.05), text="Quit Game?")
        quitButton.bind(on_press=self.quit_game)
        continueUI.add_widget(quitButton)
        self.ids['prompt_area'].add_widget(continueUI)
    
    # Function that returns game area back to original settings:
    def continue_game(self, button):
        self.ids['word_site'].font_size = '32sp'
        self.ids['word_site'].size_hint = (1, 1)
        self.ids['prompt_area'].remove_widget(button.parent)
        self.gen_word()
    
    # Function to quit the game:
    def quit_game(self, button):
        App.get_running_app().stop()

# Defines drawing area for the hangman game:
class HangmanArea(Widget):
    def drawHead(self):
        with self.canvas:
            Line(circle=(self.x + self.width * .4875, self.y + self.height * .75, self.height * .1), closed=True)
    def drawBody(self):
        with self.canvas:
            Line(points=[self.x + self.width * .4875, self.y + self.height * .65, self.x + self.width * .4875, self.y + self.height * .35])
    def drawLArm(self):
        with self.canvas:
            Line(points=[self.x + self.width * .325, self.y + self.height * .45, self.x + self.width * .4875, self.y + self.height * .6])
    def drawRArm(self):
        with self.canvas:
            Line(points=[self.x + self.width * .4875, self.y + self.height * .6, self.x + self.width * .654, self.y + self.height * .45])
    def drawLLeg(self):
        with self.canvas:
            Line(points=[self.x + self.width * .335, self.y + self.height * .10, self.x + self.width * .4875, self.y + self.height * .35])
    def drawRLeg(self):
        with self.canvas:
            Line(points=[self.x + self.width * .4875, self.y + self.height * .35, self.x + self.width * .64, self.y + self.height * .10])
    def drawGallows(self):
        with self.canvas:
            Color(0, 0, 0, mode='rgb')
            Rectangle(size=(self.width, self.height * .05), pos=self.pos)
            Rectangle(size=(self.width * .05, self.height * .90), pos=(self.x + self.width * .25, self.y))
            Rectangle(size=(self.width * .25, self.height * .05), pos=(self.x + self.width * .25, self.y + self.height * .90))
            Rectangle(size=(self.width * .025, self.height * .05), pos=(self.x + self.width * .475, self.y + self.height * .85))
    
    def draw(self, num_to_draw):
        self.canvas.clear()
        self.drawGallows()
        
        if num_to_draw > 0:
            for i in range(num_to_draw):
                if i == 0:
                    self.drawHead()
                if i == 1:
                    self.drawBody()
                if i == 2:
                    self.drawLArm()
                if i == 3:
                    self.drawRArm()
                if i == 4:
                    self.drawLLeg()
                if i == 5:
                    self.drawRLeg()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Definition of HangManApp:
class HangmanApp(App):
    
    def build(self):
        # Loads list of words on initialization:
        word_list = get_data()
        # Creates and returns HangmanGUI instance, using word_list to generate words:
        return HangmanGUI(word_list)

if __name__ == "__main__":
    app_inst = HangmanApp()
    app_inst.run()