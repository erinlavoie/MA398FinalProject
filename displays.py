# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# displays.py

import tkinter as tk
from tkinter import font


class TextDisplay(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.text_display = tk.Text(self, bg="#ffe4c8", width=110, height=35, state=tk.DISABLED)
        self.text_display.pack(side=tk.TOP, padx=5, pady=5)

        text_input_box = tk.Frame(self, bg="#a0b27f")
        text_input_box.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)

        self.text_input = tk.Text(text_input_box, width=98, height=1, state=tk.DISABLED)
        self.text_input.pack(side=tk.LEFT, padx=2, pady=2)

        self.enter_button = tk.Button(text_input_box, text="Send", width=5, state=tk.DISABLED, command=lambda: controller.handle_send)
        self.enter_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.text_display.tag_configure('USER', foreground="RED", font=font.BOLD)
        self.text_display.tag_configure('CONTACT', foreground="BLUE", font=font.BOLD)

    def get_display(self):
        return self.text_display

    def get_input(self):
        return self.text_input

    def get_button(self):
        return self.enter_button

    def display_message(self, message, tag):
        if tag == "USER":
            name = self.username
        else:
            name = self.contactname
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, name, tag)
        self.text_display.insert(tk.END, ": " + message)
        self.text_display.config(state=tk.DISABLED)