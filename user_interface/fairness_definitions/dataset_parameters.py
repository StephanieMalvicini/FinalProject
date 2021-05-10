import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from constants.outcome import NO_OUTCOME_VALUE
from databases import decision_algorithms
from handlers import input_validator
from handlers.outcome_handler import OutcomeHandler

NO_OUTCOME_DISPLAY_NAME = "Sin salida"
TEST_SIZE_DEFAULT = "25"
ERROR_TITLE = "Tamaño del conjunto de pruebas no especificado"
ERROR_DETAIL = "Por favor indique el porcentaje del conjunto de datos a utilizar para el conjunto de pruebas"


class DatasetParametersContainer:

    def __init__(self, main_frame, width, confirmed_callback, dialog):
        self.outcome_handler = OutcomeHandler()
        self.frame = \
            ttk.LabelFrame(main_frame, text="  Conjunto de datos y clasificador/algoritmo de decisión ", width=width)
        self.dataset_parameters = DatasetParameters(self.frame, self.outcome_handler,
                                                    decision_algorithms.get_all_display_names(),
                                                    confirmed_callback, dialog)


class DatasetParameters:

    def __init__(self, frame, outcome_handler, decision_algorithms_display_names, confirmed_callback, dialog):
        self.frame = ttk.Frame(frame)
        self.frame.pack(side=tk.LEFT, padx=10, pady=(7, 10))
        self.outcome_handler = outcome_handler
        self.confirmed_callback = confirmed_callback
        self.dialog = dialog
        self.filename_text, self.filename_entry = self.create_file_selector()
        self.outcome_name_combobox = self.create_outcome_name_combobox()
        self.positive_outcome_combobox = self.create_positive_outcome_combobox()
        self.test_size_spinbox = self.create_test_size_spinbox()
        self.decision_algorithm_combobox = self.create_decision_algorithm_combobox(decision_algorithms_display_names)
        self.confirm_button = self.create_confirm_button(frame)

    def create_file_selector(self):
        label = ttk.Label(self.frame, text="Archivo:")
        label.grid(column=0, row=0)
        text = tk.StringVar()
        entry = tk.Entry(self.frame, width=25, state="readonly", textvariable=text, readonlybackground="white")
        entry.grid(column=1, row=0, padx=2)
        button = ttk.Button(self.frame, text="Seleccionar", command=self.open_filename_selector)
        button.grid(column=2, row=0, padx=(0, 15))
        return text, entry

    def open_filename_selector(self):
        filename = filedialog.askopenfilename(title="Seleccionar archivo conjuto de datos",
                                              filetypes=(("CSV Files", "*.csv"),))
        if filename:
            self.outcome_handler.update_filename(filename)
            self.frame.filename = filename
            self.filename_text.set(self.frame.filename)
            self.filename_entry.after(100, self.filename_entry.xview_moveto, 1)
            self.update_outcome_name_combobox()
            self.disable_positive_outcome_combobox()
            self.confirm_button.config(state="normal")

    def create_outcome_name_combobox(self):
        label = ttk.Label(self.frame, text="Salida:")
        label.grid(column=3, row=0)
        combobox = ttk.Combobox(self.frame, state="disabled", justify="center")
        combobox.grid(column=4, row=0, padx=(2, 15))
        combobox.bind("<<ComboboxSelected>>", self.outcome_name_selected)
        return combobox

    def create_positive_outcome_combobox(self):
        label = ttk.Label(self.frame, text="Positiva:")
        label.grid(column=5, row=0)
        combobox = ttk.Combobox(self.frame, state="disabled", width=5, justify="center")
        combobox.grid(column=6, row=0, padx=(2, 15))
        combobox.bind("<<ComboboxSelected>>", self.positive_outcome_selected)
        return combobox

    def create_test_size_spinbox(self):
        label = ttk.Label(self.frame, text="Tamaño conjunto de pruebas:")
        label.grid(column=7, row=0)
        validation_command = (self.frame.register(input_validator.validate_test_size))
        spinbox = ttk.Spinbox(self.frame, from_=1, to=100, width=3, validate="key",
                              validatecommand=(validation_command, '%P'))
        spinbox.set(TEST_SIZE_DEFAULT)
        spinbox.grid(column=8, row=0, padx=(2, 1))
        percentage_label = ttk.Label(self.frame, text="%")
        percentage_label.grid(column=9, row=0, padx=(0, 15))
        return spinbox

    def create_decision_algorithm_combobox(self, display_names):
        display_names.sort()
        label = ttk.Label(self.frame, text="Nombre:")
        label.grid(column=10, row=0)
        combobox = ttk.Combobox(self.frame, state="readonly", values=display_names, justify="center")
        combobox.current(0)
        combobox.grid(column=11, row=0, padx=(2, 15))
        return combobox

    def create_confirm_button(self, frame):
        button = ttk.Button(frame, text="Confirmar", width=10, command=self.dataset_parameters_confirmed)
        button.config(state="disabled")
        button.pack(side=tk.RIGHT, padx=(0, 10), pady=(7, 10))
        return button

    def outcome_name_selected(self, _):
        outcome_name = self.outcome_name_combobox.get()
        if outcome_name == NO_OUTCOME_DISPLAY_NAME:
            outcome_name = NO_OUTCOME_VALUE
            self.outcome_handler.set_outcome_name(outcome_name)
            self.disable_positive_outcome_combobox()
        else:
            self.outcome_handler.set_outcome_name(outcome_name)
            self.update_positive_outcome_combobox()

    def update_outcome_name_combobox(self):
        columns_values = self.outcome_handler.get_all_possible_outcomes()
        columns_values.insert(0, NO_OUTCOME_DISPLAY_NAME)
        self.outcome_name_combobox["values"] = columns_values
        self.outcome_name_combobox.current(0)
        self.outcome_name_combobox.config(state="readonly")
        self.outcome_handler.set_outcome_name(NO_OUTCOME_VALUE)

    def positive_outcome_selected(self, _):
        self.outcome_handler.set_outcome_values(self.positive_outcome_combobox.get())

    def update_positive_outcome_combobox(self):
        outcome_values = self.outcome_handler.get_outcome_values()
        self.positive_outcome_combobox["values"] = outcome_values
        self.positive_outcome_combobox.current(0)
        self.positive_outcome_combobox.config(state="readonly")
        self.outcome_handler.set_outcome_values(self.positive_outcome_combobox.get())

    def disable_positive_outcome_combobox(self):
        self.positive_outcome_combobox.set("")
        self.positive_outcome_combobox.config(state="disabled")
        self.outcome_handler.set_outcome_values(None)

    def dataset_parameters_confirmed(self):
        test_size = self.test_size_spinbox.get()
        if len(test_size) == 0:
            self.dialog.show_error_with_details(ERROR_TITLE, ERROR_DETAIL)
        else:
            filename = self.outcome_handler.filename
            if self.outcome_handler.outcome_name == NO_OUTCOME_DISPLAY_NAME:
                outcome_name = NO_OUTCOME_VALUE
            else:
                outcome_name = self.outcome_handler.outcome_name
            test_size = int(test_size) / 100
            decision_algorithm_name = self.decision_algorithm_combobox.get()
            self.confirmed_callback(filename, outcome_name, test_size, decision_algorithm_name)
