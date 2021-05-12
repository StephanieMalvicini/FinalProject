import importlib
import inspect
import os
import sys
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, filedialog

from databases import decision_algorithms
from decision_algorithms import interfaces
from entities.decision_algorithm import DecisionAlgorithm
from exceptions.decision_algorithm import InvalidDecisionAlgorithmFile, ValueAlreadyExists
from user_interface.images import DecisionAlgorithmsEditorImages

FILE_ERROR_MESSAGE = "El archivo seleccionado es inválido"
DISPLAY_NAME_ERROR_TITLE = "Nombre para mostrar sin especificar"
DISPLAY_NAME_ERROR_DETAIL = "Por favor ingrese el nombre para mostrar antes de añadir"


class ParametersDisplayNames:

    def __init__(self):
        self.full_path = "Ruta completa"
        self.algorithm_display_name = "Nombre para mostrar"
        self.class_name = "Nombre de la clase"
        self.select = "Seleccionar"
        self.filedialog_algorithm = "Seleccionar archivo clasificador/algoritmo de decisión"


class DecisionAlgorithmEditor:

    def __init__(self, main_frame, dialog):
        self.frame = ttk.Frame(main_frame)
        self.frame.pack(pady=(50, 10))
        self.dialog = dialog
        self.images = DecisionAlgorithmsEditorImages()
        self.row = 2
        self.interface_classes_names = [name for (name, _) in inspect.getmembers(interfaces, inspect.isclass)]
        self.display_names = ParametersDisplayNames()
        self.create_header()
        self.filename_text = self.create_file_selector()
        self.display_name_entry = self.create_display_name_entry()
        self.class_combobox = self.create_class_combobox()
        self.add_button = self.create_add_button()
        self.create_header()
        self.create_decision_algorithm_rows()

    def create_header(self):
        my_font = font.Font(size=10)
        full_path_label = ttk.Label(self.frame, text=self.display_names.full_path, justify="center", font=my_font)
        full_path_label.grid(column=0, row=0)
        display_name_label = ttk.Label(self.frame, text=self.display_names.algorithm_display_name, justify="center",
                                       font=my_font)
        display_name_label.grid(column=1, row=0)
        class_name_label = ttk.Label(self.frame, text=self.display_names.class_name, justify="center", font=my_font)
        class_name_label.grid(column=2, row=0)

    def create_file_selector(self):
        frame = ttk.Frame(self.frame)
        frame.grid(column=0, row=1)
        text = tk.StringVar()
        entry = tk.Entry(frame, width=100, state="readonly", textvariable=text, readonlybackground="white")
        entry.grid(column=1, row=0)
        button = ttk.Button(frame, text=self.display_names.select, command=self.open_filename_selector)
        button.grid(column=2, row=0, padx=(2, 0))
        return text

    def open_filename_selector(self):
        filename = filedialog.askopenfilename(title=self.display_names.filedialog_algorithm,
                                              filetypes=(("PY Files", "*.py"),))
        if filename:
            try:
                classes_names = self.get_classes_names(filename)
                self.frame.filename = filename
                self.filename_text.set(self.frame.filename)
                self.update_class_combobox(classes_names)
                self.add_button.config(state="normal")
            except InvalidDecisionAlgorithmFile as e:
                self.dialog.show_error(FILE_ERROR_MESSAGE, e.message)
            except Exception:
                self.dialog.show_error_with_details(FILE_ERROR_MESSAGE, sys.exc_info())

    def create_display_name_entry(self):
        frame = ttk.Frame(self.frame)
        frame.grid(column=1, row=1, padx=5, pady=10)
        entry = ttk.Entry(frame, width=30, justify="center")
        entry.grid(column=1, row=0)
        return entry

    def create_class_combobox(self):
        frame = ttk.Frame(self.frame)
        frame.grid(column=2, row=1)
        combobox = ttk.Combobox(frame, state="disabled", justify="center", width=30)
        combobox.grid(column=1, row=0)
        return combobox

    def get_classes_names(self, full_path):
        classes_names = list()
        file_name = os.path.basename(full_path)
        sys.path.insert(1, full_path[0:-len(file_name)])
        module = importlib.import_module(file_name[0:-3])
        for name, _ in inspect.getmembers(module, inspect.isclass):
            if name not in self.interface_classes_names:
                classes_names.append(name)
        if len(classes_names) == 0:
            raise InvalidDecisionAlgorithmFile()
        return classes_names

    def update_class_combobox(self, classes_names):
        self.class_combobox["values"] = classes_names
        self.class_combobox.current(0)
        self.class_combobox.config(state="readonly")

    def create_add_button(self):
        button = tk.Button(self.frame, command=self.add, state="disabled", image=self.images.add,
                           highlightthickness=0, bd=0)
        button.grid(column=3, row=1, padx=10)
        return button

    def add(self):
        display_name = self.display_name_entry.get()
        if len(display_name) == 0:
            self.dialog.show_error(DISPLAY_NAME_ERROR_TITLE, DISPLAY_NAME_ERROR_DETAIL)
        else:
            try:
                class_name = self.class_combobox.get()
                decision_algorithm = DecisionAlgorithm(display_name, class_name, self.frame.filename)
                decision_algorithms.insert(decision_algorithm)
                DecisionAlgorithmRow(self.frame, self.row, decision_algorithm, self.images.delete)
                self.row += 1
            except ValueAlreadyExists as e:
                self.dialog.show_error(e.title, e.message)

    def create_decision_algorithm_rows(self):
        for decision_algorithm in decision_algorithms.get_all():
            DecisionAlgorithmRow(self.frame, self.row, decision_algorithm, self.images.delete)
            self.row += 1

    def destroy(self):
        self.frame.destroy()


class DecisionAlgorithmRow:

    def __init__(self, frame, row, decision_algorithm, image):
        self.frame = frame
        self.row = row
        self.full_path_label = self.create_full_path_label(decision_algorithm.full_path)
        self.display_name_label = self.create_display_name_label(decision_algorithm.display_name)
        self.class_name_label = self.create_class_name_label(decision_algorithm.class_name)
        self.delete_button = self.create_delete_button(image)

    def create_full_path_label(self, full_path):
        label = tk.Label(self.frame, text=full_path, borderwidth=0.5, relief="groove", bg="white")
        label.grid(column=0, row=self.row, sticky="nsew")
        return label

    def create_display_name_label(self, display_name):
        label = tk.Label(self.frame, text=display_name, borderwidth=0.5, relief="groove", bg="white")
        label.grid(column=1, row=self.row, sticky="nsew")
        return label

    def create_class_name_label(self, class_name):
        label = tk.Label(self.frame, text=class_name, borderwidth=0.5, relief="groove", bg="white")
        label.grid(column=2, row=self.row, sticky="nsew")
        return label

    def create_delete_button(self, image):
        button = tk.Button(self.frame, command=self.delete, image=image, highlightthickness=0, bd=0, height=23)
        button.grid(column=3, row=self.row)
        return button

    def delete(self):
        display_name = self.display_name_label.cget("text")
        decision_algorithms.delete(display_name)
        self.full_path_label.destroy()
        self.display_name_label.destroy()
        self.class_name_label.destroy()
        self.delete_button.destroy()


