import tkinter as tk
from tkinter import ttk

from user_interface.tree_view import create_tree_view


def show_result(satisfies, frame):
    if satisfies:
        result_text = "Satisface"
        color = "green4"
    else:
        result_text = "No satisface"
        color = "firebrick1"
    label = tk.Label(frame, text="Resultado: {}".format(result_text), fg=color)
    label.pack(anchor=tk.W)


def show_single_element(element, frame):
    label = ttk.Label(frame, text="{} = {}".format(element.name, element.value))
    label.pack(anchor=tk.W)


def show_list_element(element, frame):
    label = ttk.Label(frame, text=element.name)
    label.pack(anchor=tk.W)
    for i, item in enumerate(element.items):
        label = ttk.Label(frame, text="{} = {}".format(element.items_names[i], item))
        label.pack(anchor=tk.W)


def show_table_element(element, frame):
    label = ttk.Label(frame, text=element.name)
    label.pack(anchor=tk.W)
    create_tree_view(frame, element.column_names, element.data, max_height=4)
