import tkinter as tk
from tkinter import Toplevel, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from user_interface.plots import COLORS
from user_interface.tree_view import create_tree_view

ERROR_TOTAL_WIDTH = 400
ERROR_TOTAL_HEIGHT = 200


def show_error_detail(dialog, button, original_error):
    button.config(state="disabled")
    message = tk.Text(dialog)
    message.insert("end", original_error)
    message.config(state="disabled")
    message.pack(expand=True, fill=tk.X, side=tk.BOTTOM, pady=(0, 10), padx=5)


def create_details_button(dialog, original_error):
    details = ttk.Button(dialog, text="Ver más",
                         command=lambda: show_error_detail(dialog, details, original_error))
    details.pack(side=tk.TOP, pady=5)


def create_message(dialog, message):
    message = tk.Message(dialog, text=message, width=400, font=("", 10), justify='center')
    message.pack(side=tk.TOP, pady=(20, 0))
    return message


class CustomDialog:

    def __init__(self, window):
        self.window = window

    def create_error_dialog(self):
        dialog = Toplevel(self.window)
        dialog.geometry("{}x{}".format(ERROR_TOTAL_WIDTH, ERROR_TOTAL_HEIGHT))
        dialog.title("Error")
        dialog.iconbitmap("images/error.ico")
        return dialog

    def create_plot_dialog(self, title):
        dialog = Toplevel(self.window, bg="white")
        dialog.title(title)
        dialog.iconbitmap("images/icon.ico")
        return dialog

    def show_error_with_details(self, error_message, original_error):
        dialog = self.create_error_dialog()
        create_message(dialog, error_message)
        create_details_button(dialog, original_error)

    def show_error(self, title, message):
        dialog = self.create_error_dialog()
        create_message(dialog, title).config(fg="firebrick3")
        create_message(dialog, message)

    def show_plot(self, title, figure):
        dialog = self.create_plot_dialog(title)
        canvas = FigureCanvasTkAgg(figure, master=dialog)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)

    def show_plot_with_details(self, title, figure, button_name, details, details_title):
        dialog = self.create_plot_dialog(title)
        button = ttk.Button(dialog, text=button_name,
                            command=lambda: self.show_plot_details(details, details_title))
        button.pack(side=tk.BOTTOM, pady=10, ipady=3, ipadx=3)
        canvas = FigureCanvasTkAgg(figure, master=dialog)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)

    def show_plot_details(self, details, title):
        dialog = self.create_plot_dialog(title)
        dialog.config(bg=self.window["bg"])
        frame = ttk.Frame(dialog)
        frame.pack(padx=10, pady=10, anchor=tk.NW, fill=tk.BOTH)
        for i, item in enumerate(details):
            side_border = tk.Frame(frame, bg=COLORS[i % len(COLORS)])
            side_border.pack(anchor=tk.W, padx=(1, 0))
            label = tk.Label(side_border, text=str(item))
            label.pack(anchor=tk.W, padx=(5, 0))

    def show_testing_set(self, testing_set):
        dialog = self.create_plot_dialog("Conjunto de pruebas")
        data = testing_set.values.tolist()
        create_tree_view(dialog, list(testing_set.columns), data, max_height=len(data))
        dialog.geometry("{}x{}".format(900, 500))

