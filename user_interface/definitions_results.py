import tkinter as tk
from tkinter import ttk


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
    create_tree_view(frame, element.column_names, element.data)


def create_tree_view(parent_frame, column_names, data):
    frame = ttk.Frame(parent_frame)
    frame.pack(fill=tk.X, anchor=tk.W)
    height = 4 if len(data) >= 4 else len(data)
    tree_view = ttk.Treeview(frame, columns=column_names, show="headings", height=height)
    for column in column_names:
        tree_view.column(column, anchor=tk.CENTER)
        tree_view.heading(column, text=column)
    for row in data:
        tree_view.insert("", "end", values=row)
    # horizontal scroll
    horizontal_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree_view.xview)
    tree_view.configure(xscrollcommand=horizontal_scroll.set)
    horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    # vertical scroll
    vertical_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree_view.yview)
    vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree_view.configure(yscrollcommand=vertical_scroll.set)
    # tree view
    tree_view.pack(side=tk.TOP, anchor=tk.W)
