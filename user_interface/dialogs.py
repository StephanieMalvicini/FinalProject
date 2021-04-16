"""from tkinter import messagebox


def show_error(message, original_error):
    messagebox.showerror(message, original_error)
"""
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


class CustomDialog:

    def __init__(self, window, style):
        self.window = window
        self.style = style

    def show_error(self, message, original_error):
        bg = self.style.lookup("TFrame", "background")
        fg = self.style.lookup("TLabel", "foreground")
        dialog = Toplevel(self.window, bg=bg)
        dialog.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))
        dialog.title("Error")
        dialog.iconbitmap("images/error.ico")
        message = tk.Message(dialog, text=message, width=400, bg=bg, fg=fg, font=("", 10), justify='center')
        message.pack(side=tk.TOP, pady=(20,0))
        details = ttk.Button(dialog, text="Ver más",
                             command=lambda: show_error_detail(dialog, details, original_error))
        details.pack(side=tk.TOP, pady=5)
