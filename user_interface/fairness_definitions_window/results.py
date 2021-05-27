import tkinter as tk
from tkinter import ttk
from tkinter import font

from user_interface.tree_view import create_tree_view

SATISFIES = "Satisface"
NOT_SATISFIES = "No satisface"
RESULT = "Resultado"


def show_result(satisfies, frame):
    if satisfies:
        result_text = SATISFIES
        color = "green4"
    else:
        result_text = NOT_SATISFIES
        color = "firebrick1"
    bigger_font = font.Font(size=10)
    label = tk.Label(frame, text="{}: {}".format(RESULT, result_text), fg=color, font=bigger_font)
    label.pack(anchor=tk.W)
    elements_frame = ttk.Frame(frame)
    elements_frame.pack(anchor=tk.W, padx=5, pady=2)
    vertical_separator = ttk.Separator(elements_frame, orient="vertical")
    vertical_separator.pack(anchor=tk.W, side=tk.LEFT, fill=tk.Y, padx=5)
    return elements_frame


def show_single_element(element, frame):
    label = ttk.Label(frame, text="{} = {}".format(element.name, element.value))
    label.pack(anchor=tk.W)


def show_list_element(element, frame):
    underlined_font = font.Font(weight="bold", size=9)
    label = tk.Label(frame, text=element.name, font=underlined_font)
    label.pack(anchor=tk.W)
    for i, item in enumerate(element.items):
        label = ttk.Label(frame, text="{} = {}".format(element.items_names[i], item))
        label.pack(anchor=tk.W, padx=(10, 0))


def show_table_element(element, frame):
    underlined_font = font.Font(underline=True, size=9)
    label = tk.Label(frame, text=element.name, font=underlined_font)
    label.pack(anchor=tk.W, pady=(1, 3))
    create_tree_view(frame, element.column_names, element.data, element.max_height,
                     first_centered=element.first_column_centered)

