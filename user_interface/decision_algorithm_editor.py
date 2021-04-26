import importlib
import inspect
import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk, filedialog

from decision_algorithms import interfaces
from exceptions.invalid_decision_algorithm_class import InvalidDecisionAlgorithmFile
from exceptions.value_already_exists import ValueAlreadyExists
from handlers.decision_algorithm_handler import DecisionAlgorithmHandler

FILE_ERROR_MESSAGE = "El archivo seleccionado es inválido"
DISPLAY_NAME_ERROR_TITLE = "Nombre para mostrar sin especificar"
DISPLAY_NAME_ERROR_DETAIL = "Por favor ingrese el nombre para mostrar antes de añadir"


class DecisionAlgorithmEditor:

    def __init__(self, main_frame, dialog):
        self.frame = ttk.Frame(main_frame)
        self.frame.pack()
        self.dialog = dialog
        self.decision_algorithm_handler = DecisionAlgorithmHandler()
        self.interface_classes_names = [name for (name, _) in inspect.getmembers(interfaces, inspect.isclass)]
        self.filename_text = self.create_file_selector()
        self.display_name_entry = self.create_display_name_entry()
        self.class_combobox = self.create_class_combobox()
        self.add_button = self.create_add_button()

    def create_file_selector(self):
        label = ttk.Label(self.frame, text="Archivo: ")
        label.grid(column=0, row=0)
        text = tk.StringVar()
        entry = ttk.Entry(self.frame, width=100, state="readonly", textvariable=text)
        entry.grid(column=1, row=0)
        button = ttk.Button(self.frame, text="Seleccionar", command=self.open_filename_selector)
        button.grid(column=2, row=0)
        return text

    def open_filename_selector(self):
        filename = filedialog.askopenfilename(title="Seleccionar archivo clasificador/algoritmo de decisión",
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
        label = ttk.Label(self.frame, text="Nombre para mostrar: ")
        label.grid(column=3, row=0)
        entry = ttk.Entry(self.frame)
        entry.grid(column=4, row=0)
        return entry

    def create_class_combobox(self):
        label = ttk.Label(self.frame, text="Clase: ")
        label.grid(column=5, row=0)
        combobox = ttk.Combobox(self.frame, state="disabled", justify="center")
        combobox.grid(column=6, row=0)
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
        button = ttk.Button(self.frame, text="Añadir", command=self.add, state="disabled")
        button.grid(column=7, row=0)
        return button

    def add(self):
        display_name = self.display_name_entry.get()
        if len(display_name) == 0:
            self.dialog.show_error(DISPLAY_NAME_ERROR_TITLE, DISPLAY_NAME_ERROR_DETAIL)
        else:
            try:
                class_name = self.class_combobox.get()
                self.decision_algorithm_handler.add_decision_algorithm(display_name, class_name, self.frame.filename)
            except ValueAlreadyExists as e:
                self.dialog.show_error(e.title, e.message)

    def destroy(self):
        self.frame.destroy()

#hacer un remove -> podria mostrarlos todos y que haya un remove asociado a cada fila
#agregar aca el nuevo cada vez que se hace add

#hacer una tabla y que se pueda borrar ¿editar? cada fila
#no copiar el archivo sino que usar el path entero (tendria que crear un try catch en la creacion del objeto por si mueven o cambian algo)

#shutil.copyfile(original, target) #si ya existe uno con ese nombre se actualiza
# target = "{}/decision_algorithms/{}".format(os.getcwd().replace("\\", "/"), os.path.basename(original))