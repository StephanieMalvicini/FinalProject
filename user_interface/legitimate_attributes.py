import copy
import tkinter as tk
from numpy import number, issubdtype
from tkinter import ttk

import input_validator

COMPARISON_SIGNS_NON_NUMERIC = ["==", "!="]
COMPARISON_SIGNS_NUMERIC = ["==", "!=", ">", ">=", "<=", "<"]


class LegitimateAttributesList:

    def __init__(self, parent_frame, row):
        self.frame = tk.Frame(parent_frame)
        self.frame.grid(column=0, row=row)
        self.attributes_values = None
        self.legitimate_attributes_list = list()
        self.create_legitimate_attributes_label()
        self.add_button = self.create_add_button()
        self.add_button_row = 1

    def create_legitimate_attributes_label(self):
        group_label = tk.Label(self.frame, text="Atributos legítimos: ")
        group_label.grid(column=0, row=0)

    def create_add_button(self):
        add_button = tk.Button(self.frame, text="+", command=self.add_button_selected)
        add_button.grid(column=0, row=1)
        add_button.config(state="disabled")
        return add_button

    def add_button_selected(self):
        self.add_button_row += 1
        self.add_button.grid(column=0, row=self.add_button_row)
        self.legitimate_attributes_list.append(
            LegitimateAttributes(self.frame, self.add_button_row-1, self.attributes_values))

    def show(self, attributes_values):
        self.attributes_values = attributes_values
        self.add_button.config(state="normal")


class LegitimateAttributes:

    def __init__(self, frame, row, attributes_values):
        self.frame = frame
        self.row = row
        self.create_group_label()
        self.add_button_column = 4
        self.available_attributes = copy.deepcopy(attributes_values)
        self.numeric_attribute = False
        self.attributes_names_values = list()
        self.create_attributes_names_values()
        self.add_button = self.create_add_button()

    def create_group_label(self):
        group_name = "Grupo {}".format(self.row)
        group_label = tk.Label(self.frame, text=group_name)
        group_label.grid(column=0, row=self.row)

    def create_attributes_names_values(self):
        legitimate_attribute = dict()
        self.attributes_names_values.append(legitimate_attribute)
        legitimate_attribute["name"] = self.create_attributes_names_combobox()
        attribute_name = self.attributes_names_values[-1]["name"].get()
        self.numeric_attribute = self.attribute_is_numeric(attribute_name)
        if self.numeric_attribute:
            legitimate_attribute["comparison"] = self.create_comparison_combobox(COMPARISON_SIGNS_NUMERIC)
            legitimate_attribute["value"] = self.create_attribute_values_entry()
        else:
            legitimate_attribute["comparison"] = self.create_comparison_combobox(COMPARISON_SIGNS_NON_NUMERIC)
            legitimate_attribute["value"] = self.create_attribute_values_combobox()

    def create_attributes_names_combobox(self):
        attributes_names = list(self.available_attributes.keys())
        attributes_names_combobox = ttk.Combobox(self.frame, state="readonly", values=attributes_names)
        attributes_names_combobox.current(0)
        attributes_names_combobox.grid(column=self.add_button_column-3, row=self.row)
        attributes_names_combobox.bind("<<ComboboxSelected>>", self.attribute_name_selected)
        return attributes_names_combobox

    def attribute_name_selected(self, event):
        attribute_name = self.attributes_names_values[-1]["name"].get()
        old_attribute_is_numeric = self.numeric_attribute
        self.numeric_attribute = self.attribute_is_numeric(attribute_name)
        if self.numeric_attribute == old_attribute_is_numeric:
            if self.numeric_attribute:
                pass
            else:
                self.update_attribute_values_combobox()
        else:
            self.attributes_names_values[-1]["value"].grid_remove()
            if self.numeric_attribute:
                self.update_comparison_combobox(COMPARISON_SIGNS_NUMERIC)
                self.attributes_names_values[-1]["value"] = self.create_attribute_values_entry()
            else:
                self.update_comparison_combobox(COMPARISON_SIGNS_NON_NUMERIC)
                self.attributes_names_values[-1]["value"] = self.create_attribute_values_combobox()

    def update_comparison_combobox(self, comparison_signs):
        comparison_signs_combobox = self.attributes_names_values[-1]["value"]
        comparison_signs_combobox["values"] = comparison_signs

    def update_attribute_values_combobox(self):
        attribute_name = self.attributes_names_values[-1]["name"].get()
        attribute_values = list(self.available_attributes[attribute_name])
        attributes_values_combobox = self.attributes_names_values[-1]["value"]
        attributes_values_combobox["values"] = attribute_values
        attributes_values_combobox.current(0)

    def attribute_is_numeric(self, name):
        attribute_first_value = self.available_attributes[name][0]
        if not (isinstance(attribute_first_value, str)):
            return issubdtype(attribute_first_value, number)
        return False

    def create_comparison_combobox(self, comparison_signs):
        comparison_signs_combobox = ttk.Combobox(self.frame, state="readonly", values=comparison_signs, width=2)
        comparison_signs_combobox.current(0)
        comparison_signs_combobox.grid(column=self.add_button_column-2, row=self.row)
        return comparison_signs_combobox

    def create_attribute_values_entry(self):
        attribute_value = tk.StringVar()
        attribute_value.set(0)
        validation_command = (self.frame.register(input_validator.validate_attribute_value_numeric))
        attribute_values_entry = tk.Entry(self.frame, textvariable=attribute_value, width=10)
        attribute_values_entry.config(validate="key", validatecommand=(validation_command, '%P'))
        attribute_values_entry.grid(column=self.add_button_column-1, row=self.row)
        return attribute_values_entry

    def create_attribute_values_combobox(self):
        attribute_name = self.attributes_names_values[-1]["name"].get()
        attribute_values = list(self.available_attributes[attribute_name])
        attribute_values_combobox = ttk.Combobox(self.frame, state="readonly", values=attribute_values)
        attribute_values_combobox.current(0)
        attribute_values_combobox.grid(column=self.add_button_column-1, row=self.row)
        return attribute_values_combobox

    def create_add_button(self):
        add_button = tk.Button(self.frame, text="+", command=self.add_button_selected)
        add_button.grid(column=self.add_button_column, row=self.row)
        return add_button

    def add_button_selected(self):
        self.disable_last_attributes_names_values()
        if len(self.available_attributes) > 0:
            self.add_button_column += 3
            self.add_button.grid(column=self.add_button_column, row=self.row)
            self.create_attributes_names_values()
        else:
            self.add_button.config(state="disabled")

    def disable_last_attributes_names_values(self):
        last_legitimate_attribute = self.attributes_names_values[-1]
        last_legitimate_attribute["name"].config(state="disabled")
        attribute_name = last_legitimate_attribute["name"].get()
        del self.available_attributes[attribute_name]
        last_legitimate_attribute["comparison"].config(state="disabled")
        last_legitimate_attribute["value"].config(state="disabled")
