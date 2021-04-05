import tkinter as tk


class FairnessDefinitions:

    def __init__(self, frame):
        self.label = tk.Label(frame, text="hola")

    def show(self):
        self.label.grid(column=0, row=0)
