import copy
from numpy import number, issubdtype
from tkinter import ttk

import input_validator

COMPARISON_SIGNS_NON_NUMERIC = ["==", "!="]
COMPARISON_SIGNS_NUMERIC = ["==", "!=", ">", ">=", "<=", "<"]


class LegitimateAttributesList:

    def __init__(self, frame, row, attributes_values):
        self.frame = ttk.Frame(frame)
        self.frame.grid(columnspan=11, column=0, row=row, sticky=ttk.NW)
        self.add_button_row = 1
        self.attributes_values = attributes_values
        self.legitimate_attributes_list = list()
        self.create_legitimate_attributes_label()
        self.add_button = self.create_add_button()

    def create_legitimate_attributes_label(self):
        group_label = ttk.Label(self.frame, text="Atributos legítimos: ")
        group_label.grid(column=0, row=self.add_button_row - 1)

    def create_add_button(self):
        add_button = ttk.Button(self.frame, text="+", command=self.add_button_selected)
        add_button.grid(column=0, row=self.add_button_row)
        return add_button

    def add_button_selected(self):
        self.add_button_row += 1
        self.add_button.grid(column=0, row=self.add_button_row)
        self.legitimate_attributes_list.append(
            LegitimateAttributes(self.frame, self.add_button_row - 1, self.attributes_values))


class LegitimateAttributes:

    def __init__(self, frame, row, attributes_values):
        self.frame = frame
        self.row = row
        self.create_group_label()
        self.add_button_column = 4
        self.attributes_values = attributes_values
        self.available_attributes = copy.deepcopy(attributes_values)
        self.legitimate_attributes = list()
        self.create_legitimate_attribute()
        self.add_button = self.create_add_button()

    def create_group_label(self):
        group_name = "Grupo {}".format(self.row)
        group_label = ttk.Label(self.frame, text=group_name)
        group_label.grid(column=0, row=self.row)

    def create_legitimate_attribute(self):
        self.legitimate_attributes.append(LegitimateAttribute(
            self.frame, self.available_attributes, self.row, self.add_button_column))

    def create_add_button(self):
        add_button = ttk.Button(self.frame, text="+", command=self.add_button_selected)
        add_button.grid(column=self.add_button_column, row=self.row)
        return add_button

    def add_button_selected(self):
        last_legitimate_attribute = self.legitimate_attributes[-1]
        last_legitimate_attribute.disable()
        attribute_name = last_legitimate_attribute.get_attribute_name()
        del self.available_attributes[attribute_name]
        if len(self.available_attributes) > 0:
            self.add_button_column += 3
            self.add_button.grid(column=self.add_button_column, row=self.row)
            self.create_legitimate_attribute()
        else:
            self.add_button.config(state="disabled")


class LegitimateAttribute:

    def __init__(self, frame, available_attributes, row, add_button_column):
        self.frame = frame
        self.available_attributes = available_attributes
        self.row = row
        self.add_button_column = add_button_column
        self.attributes_names_combobox = self.create_attributes_names_combobox()
        self.attribute_values_entry = self.create_attribute_values_entry()
        self.attribute_values_combobox = self.create_attribute_values_combobox()
        if self.attribute_is_numeric(self.attributes_names_combobox.get()):
            self.comparison_signs_combobox = self.create_comparison_signs_combobox(COMPARISON_SIGNS_NUMERIC)
            self.current_attribute_values = self.attribute_values_entry
            self.numeric_attribute = True
        else:
            self.comparison_signs_combobox = self.create_comparison_signs_combobox(COMPARISON_SIGNS_NUMERIC)
            self.current_attribute_values = self.attribute_values_combobox
            self.numeric_attribute = False
        self.current_attribute_values.grid(column=self.add_button_column - 1, row=self.row)

    def create_attributes_names_combobox(self):
        attributes_names = list(self.available_attributes.keys())
        attributes_names_combobox = ttk.Combobox(self.frame, state="readonly", values=attributes_names)
        attributes_names_combobox.current(0)
        attributes_names_combobox.grid(column=self.add_button_column - 3, row=self.row)
        attributes_names_combobox.bind("<<ComboboxSelected>>", self.attribute_name_selected)
        return attributes_names_combobox

    def attribute_name_selected(self, event):
        attribute_name = self.attributes_names_combobox.get()
        old_attribute_is_numeric = self.numeric_attribute
        self.numeric_attribute = self.attribute_is_numeric(attribute_name)
        if self.numeric_attribute != old_attribute_is_numeric:
            self.current_attribute_values.grid_remove()
            if self.numeric_attribute:
                self.update_comparison_signs_combobox(COMPARISON_SIGNS_NUMERIC)
                self.current_attribute_values = self.attribute_values_entry
            else:
                self.update_comparison_signs_combobox(COMPARISON_SIGNS_NON_NUMERIC)
                self.current_attribute_values = self.attribute_values_combobox
            self.current_attribute_values.grid(column=self.add_button_column - 1, row=self.row)
        else:
            if not self.numeric_attribute:
                self.update_attribute_values_combobox()

    def update_comparison_signs_combobox(self, comparison_signs):
        self.comparison_signs_combobox["values"] = comparison_signs

    def update_attribute_values_combobox(self):
        attribute_name = self.attributes_names_combobox.get()
        attribute_values = list(self.available_attributes[attribute_name])
        self.attributes_values_combobox["values"] = attribute_values
        self.attributes_values_combobox.current(0)

    def attribute_is_numeric(self, name):
        attribute_first_value = self.available_attributes[name][0]
        if not (isinstance(attribute_first_value, str)):
            return issubdtype(attribute_first_value, number)
        return False

    def create_comparison_signs_combobox(self, comparison_signs):
        comparison_signs_combobox = ttk.Combobox(self.frame, state="readonly", values=comparison_signs, width=2)
        comparison_signs_combobox.current(0)
        comparison_signs_combobox.grid(column=self.add_button_column - 2, row=self.row)
        return comparison_signs_combobox

    def create_attribute_values_entry(self):
        attribute_value = ttk.StringVar()
        attribute_value.set(0)
        validation_command = (self.frame.register(input_validator.validate_attribute_value_numeric))
        attribute_values_entry = ttk.Entry(self.frame, textvariable=attribute_value, width=10)
        attribute_values_entry.config(validate="key", validatecommand=(validation_command, '%P'))
        return attribute_values_entry

    def create_attribute_values_combobox(self):
        attribute_name = self.attributes_names_combobox.get()
        attribute_values = list(self.available_attributes[attribute_name])
        attribute_values_combobox = ttk.Combobox(self.frame, state="readonly", values=attribute_values)
        attribute_values_combobox.current(0)
        return attribute_values_combobox

    def disable(self):
        self.attributes_names_combobox.config(state="disabled")
        self.comparison_signs_combobox.config(state="disabled")
        self.attribute_values_entry.config(state="disabled")
        self.attribute_values_combobox.config(state="disabled")

    def get_attribute_name(self):
        return self.attributes_names_combobox.get()
