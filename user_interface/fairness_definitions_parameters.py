import tkinter as tk
from tkinter import ttk

from exceptions.parameter_not_defined import ParameterNotDefined
from handlers import input_validator
from constants.statistical_constants import CONFIDENCE_Z_VALUES
from user_interface.legitimate_attributes import LegitimateAttributesList

MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT = 0.01
ERROR_DEFAULT = 0.01
MINIMUM_SAMPLES_AMOUNT_DEFAULT = 1
DECIMALS_DEFAULT = 0
MINIMUM_SAMPLES_AMOUNT_ERROR_TITLE = "Mínima cantidad de pruebas sin especificar"
MINIMUM_SAMPLES_AMOUNT_ERROR_DETAIL = "Por favor ingrese la cantidad mínima de pruebas para continuar"


class FairnessDefinitionsParametersContainer:

    def __init__(self, main_frame, width, dialog):
        self.frame = \
            ttk.LabelFrame(main_frame, text="  Definiciones de fairness - parámetros  ", height=200, width=width)
        self.fairness_definitions_parameters = None
        self.dialog = dialog

    def update(self, dataset_handler, required_parameters_names):
        if self.fairness_definitions_parameters:
            self.fairness_definitions_parameters.destroy()
        self.fairness_definitions_parameters = \
            FairnessDefinitionsParameters(self.frame,
                                          dataset_handler.get_testing_dataset_samples_amount(),
                                          dataset_handler.get_attributes_values(),
                                          required_parameters_names,
                                          self.dialog)


class FairnessDefinitionsParameters:

    def __init__(self, parent_frame, max_samples, attributes_values, required_parameters_names, dialog):
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(side=tk.TOP)
        self.required_parameters = dict()
        self.create_maximum_acceptable_difference_spinbox(required_parameters_names)
        self.create_confidence_combobox(required_parameters_names)
        self.create_error_spinbox(required_parameters_names)
        self.create_minimum_samples_amount_spinbox(max_samples, required_parameters_names)
        self.create_decimals_spinbox(required_parameters_names)
        self.legitimate_attributes_list_frame = \
            self.create_legitimate_attributes_list(parent_frame, attributes_values, dialog, required_parameters_names)

    def create_maximum_acceptable_difference_spinbox(self, required_parameters_names):
        label = ttk.Label(self.frame, text="Diferencia aceptable: ")
        label.grid(column=1, row=0)
        validation_command = (self.frame.register(input_validator.validate_maximum_acceptable_difference))
        spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01, width=4, validate="key",
                              validatecommand=(validation_command, '%P'))
        spinbox.set(MAXIMUM_ACCEPTABLE_DIFFERENCE_DEFAULT)
        spinbox.grid(column=2, row=0)
        if "maximum_acceptable_difference" not in required_parameters_names:
            spinbox.config(state="disabled")
        else:
            self.required_parameters["maximum_acceptable_difference"] = spinbox

    def create_confidence_combobox(self, required_parameters_names):
        label = ttk.Label(self.frame, text="Confianza: ")
        label.grid(column=3, row=0)
        confidence_values = list(CONFIDENCE_Z_VALUES.keys())
        combobox = ttk.Combobox(self.frame, state="readonly", values=confidence_values, width=2)
        combobox.current(0)
        combobox.grid(column=4, row=0)
        percentage_label = ttk.Label(self.frame, text="%")
        percentage_label.grid(column=5, row=0)
        if "confidence" not in required_parameters_names:
            combobox.config(state="disabled")
        else:
            self.required_parameters["confidence"] = combobox

    def create_error_spinbox(self, required_parameters_names):
        label = ttk.Label(self.frame, text="Máximo error: ")
        label.grid(column=6, row=0)
        validation_command = (self.frame.register(input_validator.validate_error))
        spinbox = ttk.Spinbox(self.frame, from_=0, to=1, increment=0.01, width=4, validate="key",
                              validatecommand=(validation_command, '%P'))
        spinbox.set(ERROR_DEFAULT)
        spinbox.grid(column=7, row=0)
        if "error" not in required_parameters_names:
            spinbox.config(state="disabled")
        else:
            self.required_parameters["error"] = spinbox

    def create_minimum_samples_amount_spinbox(self, max_samples, required_parameters_names):
        label = ttk.Label(self.frame, text="Mínima cantidad de pruebas: ")
        label.grid(column=8, row=0)
        validation_command = (self.frame.register(input_validator.validate_minimum_samples_amount))
        spinbox = ttk.Spinbox(self.frame, from_=1, to=max_samples, width=6, validate="key",
                              validatecommand=(validation_command, '%P', max_samples))
        spinbox.set(MINIMUM_SAMPLES_AMOUNT_DEFAULT)
        spinbox.grid(column=9, row=0)
        if "minimum_samples_amount" not in required_parameters_names:
            spinbox.config(state="disabled")
        else:
            self.required_parameters["minimum_samples_amount"] = spinbox

    def create_decimals_spinbox(self, required_parameters_names):
        label = ttk.Label(self.frame, text="Decimales probabilidad: ")
        label.grid(column=10, row=0)
        validation_command = (self.frame.register(input_validator.validate_decimals))
        spinbox = ttk.Spinbox(self.frame, from_=0, to=5, width=1, validate="key",
                              validatecommand=(validation_command, '%P'))
        spinbox.set(DECIMALS_DEFAULT)
        spinbox.grid(column=11, row=0)
        if "decimals" not in required_parameters_names:
            spinbox.config(state="disabled")
        else:
            self.required_parameters["decimals"] = spinbox

    def create_legitimate_attributes_list(self, parent_frame, attributes_values, dialog, required_parameters_names):
        required = "legitimate_attributes_list" in required_parameters_names
        frame = ttk.Frame(parent_frame)
        frame.pack(side=tk.LEFT)
        legitimate_attributes_list = LegitimateAttributesList(frame, 1, attributes_values, required, dialog)
        if required:
            self.required_parameters["legitimate_attributes_list"] = legitimate_attributes_list
        return frame

    def get_parameters_values(self):
        minimum_samples_amount = self.required_parameters["minimum_samples_amount"]
        if minimum_samples_amount and len(minimum_samples_amount.get()) == 0:
            raise ParameterNotDefined(MINIMUM_SAMPLES_AMOUNT_ERROR_TITLE, MINIMUM_SAMPLES_AMOUNT_ERROR_DETAIL)
        parameters_values = dict()
        for parameter, widget in self.required_parameters.items():
            parameters_values[parameter] = widget.get()
        return parameters_values

    def destroy(self):
        self.frame.destroy()
        self.legitimate_attributes_list_frame.destroy()
