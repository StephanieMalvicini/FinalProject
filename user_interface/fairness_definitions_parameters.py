from tkinter import ttk

import input_validator
from statistical_constants import CONFIDENCE_Z_VALUES
from user_interface.legitimate_attributes import LegitimateAttributesList

MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT = 0.01
ERROR_DEFAULT = 0.01
MINIMUM_SAMPLES_AMOUNT_DEFAULT = 1
DECIMALS_DEFAULT = 0


class FairnessDefinitionsParameters:

    def __init__(self, parent_frame, dataset_handler):
        self.frame = ttk.Frame(parent_frame)
        self.frame.grid(columnspan=11, column=0, row=0, sticky=tk.NW)
        self.dataset_handler = dataset_handler
        self.maximum_acceptable_difference_spinbox = self.create_maximum_acceptable_difference_spinbox()
        self.confidence_combobox = self.create_confidence_combobox()
        self.error_spinbox = self.create_error_spinbox()
        self.minimum_samples_amount_spinbox = self.create_minimum_samples_amount_spinbox()
        self.decimals_spinbox = self.create_decimals_spinbox()
        self.legitimate_attributes_list = LegitimateAttributesList(parent_frame, 1,
                                                                   dataset_handler.get_attributes_values())

    def create_maximum_acceptable_difference_spinbox(self):
        maximum_acceptable_difference_label = ttk.Label(self.frame, text="Diferencia aceptable: ")
        maximum_acceptable_difference_label.grid(column=1, row=0)
        maximum_acceptable_difference_text = ttk.StringVar()
        maximum_acceptable_difference_text.set(MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT)
        validation_command = (self.frame.register(input_validator.validate_maximum_acceptable_difference))
        maximum_acceptable_difference_spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01,
                                                           textvariable=maximum_acceptable_difference_text, width=4)
        maximum_acceptable_difference_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        maximum_acceptable_difference_spinbox.grid(column=2, row=0)
        return maximum_acceptable_difference_spinbox

    def create_confidence_combobox(self):
        confidence_label = ttk.Label(self.frame, text="Confianza: ")
        confidence_label.grid(column=3, row=0)
        confidence_values = list(CONFIDENCE_Z_VALUES.keys())
        confidence_combobox = ttk.Combobox(self.frame, state="readonly", values=confidence_values, width=2)
        confidence_combobox.current(0)
        confidence_combobox.grid(column=4, row=0)
        percentage_label = ttk.Label(self.frame, text="%")
        percentage_label.grid(column=5, row=0)
        return confidence_combobox

    def create_error_spinbox(self):
        error_label = ttk.Label(self.frame, text="Máximo error: ")
        error_label.grid(column=6, row=0)
        error_text = ttk.StringVar()
        error_text.set(ERROR_DEFAULT)
        validation_command = (self.frame.register(input_validator.validate_error))
        error_spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01, textvariable=error_text, width=4)
        error_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        error_spinbox.grid(column=7, row=0)
        return error_spinbox

    def create_minimum_samples_amount_spinbox(self):
        minimum_samples_amount_label = ttk.Label(self.frame, text="Mínima cantidad de pruebas: ")
        minimum_samples_amount_label.grid(column=8, row=0)
        minimum_samples_amount_text = ttk.StringVar()
        minimum_samples_amount_text.set(MINIMUM_SAMPLES_AMOUNT_DEFAULT)
        max_samples = self.dataset_handler.get_testing_dataset_samples_amount()
        validation_command = (self.frame.register(input_validator.validate_minimum_samples_amount))
        minimum_samples_amount_spinbox = ttk.Spinbox(self.frame, from_=1, to=max_samples,
                                                    textvariable=minimum_samples_amount_text, width=6)
        minimum_samples_amount_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        minimum_samples_amount_spinbox.grid(column=9, row=0)
        return minimum_samples_amount_spinbox

    def create_decimals_spinbox(self):
        decimals_label = ttk.Label(self.frame, text="Decimales probabilidad: ")
        decimals_label.grid(column=10, row=0)
        decimals_text = ttk.StringVar()
        decimals_text.set(ERROR_DEFAULT)
        validation_command = (self.frame.register(input_validator.validate_decimals))
        decimals_spinbox = ttk.Spinbox(self.frame, from_=0, to=5, textvariable=decimals_text, width=1)
        decimals_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        decimals_spinbox.grid(column=11, row=0)
        return decimals_spinbox
