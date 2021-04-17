import tkinter as tk
from tkinter import ttk

from handlers import input_validator
from constants.statistical_constants import CONFIDENCE_Z_VALUES
from user_interface.legitimate_attributes import LegitimateAttributesList

MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT = 0.01
ERROR_DEFAULT = 0.01
MINIMUM_SAMPLES_AMOUNT_DEFAULT = 1
DECIMALS_DEFAULT = 0


class FairnessDefinitionsParametersContainer:

    def __init__(self, main_frame, width, dialog):
        self.frame = \
            ttk.LabelFrame(main_frame, text="  Definiciones de fairness - parámetros  ", height=200, width=width)
        self.fairness_definitions_parameters = None
        self.dialog = dialog

    def update(self, dataset_handler, fairness_definitions_parameters_handler):
        if self.fairness_definitions_parameters:
            self.fairness_definitions_parameters.destroy()
        self.fairness_definitions_parameters = \
            FairnessDefinitionsParameters(self.frame,
                                          dataset_handler.get_testing_dataset_samples_amount(),
                                          dataset_handler.get_attributes_values(),
                                          fairness_definitions_parameters_handler.get_required_parameters_names(),
                                          self.dialog)


class FairnessDefinitionsParameters:

    def __init__(self, parent_frame, max_samples, attributes_values, required_parameters_names, dialog):
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(side=tk.TOP)
        self.required_parameters_names = required_parameters_names
        self.maximum_acceptable_difference_spinbox = self.create_maximum_acceptable_difference_spinbox()
        self.confidence_combobox = self.create_confidence_combobox()
        self.error_spinbox = self.create_error_spinbox()
        self.minimum_samples_amount_spinbox = self.create_minimum_samples_amount_spinbox(max_samples)
        self.decimals_spinbox = self.create_decimals_spinbox()
        legitimate_attributes_required = "legitimate_attributes_list" in required_parameters_names
        self.legitimate_attributes_list_frame = ttk.Frame(parent_frame)
        self.legitimate_attributes_list_frame.pack(side=tk.LEFT)
        self.legitimate_attributes_list = LegitimateAttributesList(self.legitimate_attributes_list_frame, 1,
                                                                   attributes_values,
                                                                   legitimate_attributes_required, dialog)

    def create_maximum_acceptable_difference_spinbox(self):
        maximum_acceptable_difference_label = ttk.Label(self.frame, text="Diferencia aceptable: ")
        maximum_acceptable_difference_label.grid(column=1, row=0)
        validation_command = (self.frame.register(input_validator.validate_maximum_acceptable_difference))
        maximum_acceptable_difference_spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01, width=4)
        maximum_acceptable_difference_spinbox.set(MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT)
        maximum_acceptable_difference_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        maximum_acceptable_difference_spinbox.grid(column=2, row=0)
        if "Diferencia aceptable" not in self.required_parameters_names:
            maximum_acceptable_difference_spinbox.config(state="disabled")
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
        if "maximum_acceptable_difference" not in self.required_parameters_names:
            confidence_combobox.config(state="disabled")
        return confidence_combobox

    def create_error_spinbox(self):
        error_label = ttk.Label(self.frame, text="Máximo error: ")
        error_label.grid(column=6, row=0)
        validation_command = (self.frame.register(input_validator.validate_error))
        error_spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01, width=4)
        error_spinbox.set(ERROR_DEFAULT)
        error_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        error_spinbox.grid(column=7, row=0)
        if "error" not in self.required_parameters_names:
            error_spinbox.config(state="disabled")
        return error_spinbox

    def create_minimum_samples_amount_spinbox(self, max_samples):
        minimum_samples_amount_label = ttk.Label(self.frame, text="Mínima cantidad de pruebas: ")
        minimum_samples_amount_label.grid(column=8, row=0)
        validation_command = (self.frame.register(input_validator.validate_minimum_samples_amount))
        minimum_samples_amount_spinbox = ttk.Spinbox(self.frame, from_=1, to=max_samples, width=6)
        minimum_samples_amount_spinbox.set(MINIMUM_SAMPLES_AMOUNT_DEFAULT)
        minimum_samples_amount_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        minimum_samples_amount_spinbox.grid(column=9, row=0)
        if "minimum_samples_amount" not in self.required_parameters_names:
            minimum_samples_amount_spinbox.config(state="disabled")
        return minimum_samples_amount_spinbox

    def create_decimals_spinbox(self):
        decimals_label = ttk.Label(self.frame, text="Decimales probabilidad: ")
        decimals_label.grid(column=10, row=0)
        validation_command = (self.frame.register(input_validator.validate_decimals))
        decimals_spinbox = ttk.Spinbox(self.frame, from_=0, to=5, width=1)
        decimals_spinbox.set(DECIMALS_DEFAULT)
        decimals_spinbox.config(validate="key", validatecommand=(validation_command, '%P'))
        decimals_spinbox.grid(column=11, row=0)
        if "decimals" not in self.required_parameters_names:
            decimals_spinbox.config(state="disabled")
        return decimals_spinbox

    def destroy(self):
        self.frame.destroy()
        self.legitimate_attributes_list_frame.destroy()
