import tkinter as tk
from tkinter import Toplevel, ttk

TOTAL_WIDTH = 400
TOTAL_HEIGHT = 200


def show_error_detail(dialog, button, original_error):
    button.config(state="disabled")
    message = tk.Text(dialog)
    message.insert("end", original_error)
    message.config(state="disabled")
    message.pack(expand=True, fill=tk.X, side=tk.BOTTOM, pady=(0,10), padx=5)


def create_details_button(dialog, original_error):
    details = ttk.Button(dialog, text="Ver más",
                         command=lambda: show_error_detail(dialog, details, original_error))
    details.pack(side=tk.TOP, pady=5)


class CustomDialog:

    def __init__(self, window, style):
        self.window = window
        self.bg = style.lookup("TFrame", "background")
        self.fg = style.lookup("TLabel", "foreground")

    def create_dialog(self, title):
        dialog = Toplevel(self.window, bg=self.bg)
        dialog.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))
        dialog.title(title)
        dialog.iconbitmap("images/error.ico")
        return dialog

    def create_message(self, dialog, message):
        message = tk.Message(dialog, text=message, width=400, bg=self.bg, fg=self.fg, font=("", 10), justify='center')
        message.pack(side=tk.TOP, pady=(20,0))
        return message

    def show_error_with_details(self, error_message, original_error):
        dialog = self.create_dialog("Error")
        self.create_message(dialog, error_message)
        create_details_button(dialog, original_error)

    def show_error(self, title, message):
        dialog = self.create_dialog("Error")
        self.create_message(dialog, title).config(fg="firebrick3")
        self.create_message(dialog, message)

    def update_style(self, style):
        self.bg = style.lookup("TFrame", "background")
        self.fg = style.lookup("TLabel", "foreground")
