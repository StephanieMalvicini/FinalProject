from tkinter import ttk
import tkinter as tk


def create_tree_view(parent_frame, column_names, data, max_height):
    frame = ttk.Frame(parent_frame)
    frame.pack(fill=tk.X, anchor=tk.W)
    height = max_height if len(data) >= max_height else len(data)
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