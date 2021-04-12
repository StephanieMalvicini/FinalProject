from tkinter import ttk
from tkinter import filedialog

import input_validator

NO_OUTCOME_DISPLAY_NAME = "Sin salida"
NO_OUTCOME_VALUE = ""
TEST_SIZE_DEFAULT = "25"


class DatasetParameters:
    def __init__(self, frame, outcome_handler, gui):
        self.frame = frame
        self.outcome_handler = outcome_handler
        self.gui = gui

        self.filename_text, self.filename_entry, self.filename_button = self.create_file_selector()
        self.outcome_name_combobox = self.create_outcome_name_combobox()
        self.positive_outcome_combobox = self.create_positive_outcome_combobox()
        self.test_size_spinbox = self.create_test_size_spinbox()
        self.confirm_button = self.create_confirm_button()

    def create_file_selector(self):
        filename_label = ttk.Label(self.frame, text="Archivo: ")
        filename_label.grid(column=0, row=0)
        filename_text = ttk.StringVar()
        filename_entry = ttk.Entry(self.frame, width=25, state="readonly", textvariable=filename_text)
        filename_entry.grid(column=1, row=0)
        filename_select_button = ttk.Button(self.frame, text="Seleccionar", command=self.open_filename_selector)
        filename_select_button.grid(column=2, row=0)
        return filename_text, filename_entry, filename_select_button

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
            self.confirm_button.config(state='normal')

    def create_outcome_name_combobox(self):
        outcome_name_label = ttk.Label(self.frame, text="Salida: ")
        outcome_name_label.grid(column=3, row=0)
        outcome_name_combobox = ttk.Combobox(self.frame, state="readonly")
        outcome_name_combobox.config(state='disabled')
        outcome_name_combobox.grid(column=4, row=0)
        outcome_name_combobox.bind("<<ComboboxSelected>>", self.outcome_name_selected)
        return outcome_name_combobox

    def outcome_name_selected(self, *args):
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
        self.outcome_name_combobox.config(state='enabled')
        self.outcome_handler.set_outcome_name(NO_OUTCOME_VALUE)

    def create_positive_outcome_combobox(self):
        positive_outcome_label = ttk.Label(self.frame, text="Positiva: ")
        positive_outcome_label.grid(column=5, row=0)
        positive_outcome_combobox = ttk.Combobox(self.frame, state="readonly")
        positive_outcome_combobox.config(state='disabled')
        positive_outcome_combobox.grid(column=6, row=0)
        positive_outcome_combobox.bind("<<ComboboxSelected>>", self.positive_outcome_selected)
        return positive_outcome_combobox

    def positive_outcome_selected(self, *args):
        self.outcome_handler.set_outcome_values(self.positive_outcome_combobox.get())

    def update_positive_outcome_combobox(self):
        outcome_values = self.outcome_handler.get_outcome_values()
        self.positive_outcome_combobox["values"] = outcome_values
        self.positive_outcome_combobox.current(0)
        self.positive_outcome_combobox.config(state='enabled')
        self.outcome_handler.set_outcome_values(self.positive_outcome_combobox.get())

    def disable_positive_outcome_combobox(self):
        self.positive_outcome_combobox.set("")
        self.positive_outcome_combobox.config(state='disabled')
        self.outcome_handler.set_outcome_values(None)

    def create_test_size_spinbox(self):
        test_size_label = ttk.Label(self.frame, text="Tamaño conjunto de pruebas: ")
        test_size_label.grid(column=7, row=0)
        test_size_text = ttk.StringVar()
        test_size_text.set(TEST_SIZE_DEFAULT)
        validation_command = (self.frame.register(input_validator.validate_test_size))
        test_size_spinbox = ttk.Spinbox(self.frame, from_=1, to=100, textvariable=test_size_text, width=3)
        test_size_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        test_size_spinbox.grid(column=8, row=0)
        percentage_label = ttk.Label(self.frame, text="%")
        percentage_label.grid(column=9, row=0)
        return test_size_spinbox

    def create_confirm_button(self):
        confirm_button = ttk.Button(self.frame, text="Confirmar", command=self.dataset_parameters_confirmed)
        confirm_button.config(state="disabled")
        confirm_button.grid(column=10, row=0)
        return confirm_button

    def dataset_parameters_confirmed(self):
        filename = self.outcome_handler.filename
        outcome_name = self.outcome_handler.outcome_name
        test_size = int(self.test_size_spinbox.get())/100
        self.gui.dataset_parameters_confirmed(filename, outcome_name, test_size)



