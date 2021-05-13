import tkinter as tk
import copy
from math import ceil

from numpy import number, issubdtype
from tkinter import ttk

from exceptions.parameters import ParameterNotDefined
from handlers import input_validator
from user_interface.images import LegitimateAttributesImages

COMPARISON_SIGNS_NON_NUMERIC = ["==", "!="]
COMPARISON_SIGNS_NUMERIC = ["==", "!=", ">", ">=", "<=", "<"]
AMOUNT_PER_ROW = 4

GROUP_LABEL = "Grupo"
ERROR_TITLE_GROUP = "Grupo {}: valor del atributo {} no especificado"
ERROR_DETAIL_GROUP = "Por favor introduzca el valor del atributo {} para realizar la comparación"
ERROR_TITLE = "Atributos legítimos sin especificar"
ERROR_DETAIL = "Por favor añada al menos un atributo legítimo para continuar"


class LegitimateAttributesList:

    def __init__(self, frame, row, attributes_values, required, dialog, display_names):
        self.frame = ttk.Frame(frame)
        self.frame.grid(column=0, row=row, sticky=tk.NW)
        self.button_row = 1
        self.attributes_values = attributes_values
        self.dialog = dialog
        self.images = LegitimateAttributesImages()
        self.legitimate_attributes_list = list()
        self.create_legitimate_attributes_label(display_names)
        self.buttons_frame, self.add_button, self.remove_button = self.create_add_remove_buttons()
        self.add_button_selected()
        if not required:
            self.add_button.config(state="disabled")
            self.remove_button.config(state="disabled")
            self.legitimate_attributes_list[0].disable()

    def create_legitimate_attributes_label(self, display_names):
        label = ttk.Label(self.frame, text="{}:".format(display_names["legitimate_attributes_list"]))
        label.grid(sticky=tk.W, column=0, row=self.button_row - 1, columnspan=2)

    def create_add_remove_buttons(self):
        frame = ttk.Frame(self.frame)
        frame.grid(column=0, row=self.button_row, pady=(2, 10))
        add_button = tk.Button(frame, command=self.add_button_selected, image=self.images.add, highlightthickness=0,
                               bd=0)
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        remove_button = tk.Button(frame, command=self.remove_button_selected, state="disabled",
                                  image=self.images.remove,
                                  highlightthickness=0, bd=0)
        remove_button.pack(side=tk.RIGHT)
        return frame, add_button, remove_button

    def add_button_selected(self):
        start_row = self.button_row
        self.button_row = self.button_row + ceil(len(self.attributes_values) / AMOUNT_PER_ROW)
        self.buttons_frame.grid(column=0, row=self.button_row, pady=(2, 10))
        self.remove_button.config(state="normal")
        self.legitimate_attributes_list.append(LegitimateAttributes(self.frame, start_row, self.attributes_values,
                                                                    len(self.legitimate_attributes_list) + 1,
                                                                    self.dialog, self.images))

    def remove_button_selected(self):
        last = self.legitimate_attributes_list[-1]
        last.remove()
        del self.legitimate_attributes_list[-1]
        self.button_row = self.button_row - int(len(self.attributes_values) / AMOUNT_PER_ROW)
        self.buttons_frame.grid(column=0, row=self.button_row, pady=(2, 10))
        if len(self.legitimate_attributes_list) == 0:
            self.remove_button.config(state="disabled")

    def get(self):
        if len(self.legitimate_attributes_list) == 0:
            raise ParameterNotDefined(ERROR_TITLE, ERROR_DETAIL)
        legitimate_attributes_values = list()
        for legitimate_attributes in self.legitimate_attributes_list:
            legitimate_attributes_values.append(legitimate_attributes.get())
        return legitimate_attributes_values


class LegitimateAttributes:

    def __init__(self, frame, start_row, attributes_values, group_number, dialog, images):
        self.frame = frame
        self.row = start_row
        self.group_number = group_number
        self.group_label = self.create_group_label()
        self.add_button_column = 4
        self.attributes_values = attributes_values
        self.dialog = dialog
        self.images = images
        self.available_attributes = copy.deepcopy(attributes_values)
        self.legitimate_attributes = list()
        self.create_legitimate_attribute()
        self.buttons_frame, self.add_button, self.remove_button = self.create_add_remove_buttons()

    def update_column_and_row_on_add(self):
        if len(self.legitimate_attributes) % AMOUNT_PER_ROW == 0:
            self.add_button_column = 1
            self.row += 1

    def update_column_and_row_on_remove(self):
        if len(self.legitimate_attributes) % AMOUNT_PER_ROW == 0:
            self.add_button_column = 3 * AMOUNT_PER_ROW + 1
            self.row -= 1
        else:
            self.add_button_column -= 3

    def create_group_label(self):
        group_name = "{} {}".format(GROUP_LABEL, self.group_number)
        label = ttk.Label(self.frame, text=group_name)
        label.grid(column=0, row=self.row, padx=10)
        return label

    def create_legitimate_attribute(self):
        self.legitimate_attributes.append(LegitimateAttribute(
            self.frame, self.available_attributes, self.row, self.add_button_column, self.group_number))

    def create_add_remove_buttons(self):
        frame = ttk.Frame(self.frame)
        frame.grid(column=self.add_button_column, row=self.row)
        add_button = tk.Button(frame, command=self.add_button_selected, image=self.images.add,
                               highlightthickness=0, bd=0)
        add_button.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 10))
        remove_button = tk.Button(frame, command=self.remove_button_selected, state="disabled",
                                  image=self.images.remove, highlightthickness=0, bd=0)
        remove_button.pack(side=tk.LEFT, anchor=tk.W)
        return frame, add_button, remove_button

    def add_button_selected(self):
        last_legitimate_attribute = self.legitimate_attributes[-1]
        if last_legitimate_attribute.value_is_empty():
            attribute_name = last_legitimate_attribute.get_attribute_name()
            self.dialog.show_error(ERROR_TITLE_GROUP.format(self.group_number, attribute_name),
                                   ERROR_DETAIL_GROUP.format(attribute_name))
        else:
            last_legitimate_attribute.disable()
            attribute_name = last_legitimate_attribute.get_attribute_name()
            del self.available_attributes[attribute_name]
            self.update_column_and_row_on_add()
            self.remove_button.config(state="normal")
            if len(self.available_attributes) > 0:
                self.add_button_column += 3
                self.buttons_frame.grid(column=self.add_button_column, row=self.row)
                self.create_legitimate_attribute()
            else:
                self.add_button.config(state="disabled")

    def remove_button_selected(self):
        last_legitimate_attribute = self.legitimate_attributes[-1]
        del self.legitimate_attributes[-1]
        self.update_column_and_row_on_remove()
        attribute_name = last_legitimate_attribute.get_attribute_name()
        self.available_attributes[attribute_name] = self.attributes_values[attribute_name]
        last_legitimate_attribute.remove()
        new_last_legitimate_attribute = self.legitimate_attributes[-1]
        attribute_name = new_last_legitimate_attribute.get_attribute_name()
        self.available_attributes[attribute_name] = self.attributes_values[attribute_name]
        new_last_legitimate_attribute.enable()
        self.buttons_frame.grid(column=self.add_button_column, row=self.row)
        if len(self.legitimate_attributes) == 1:
            self.remove_button.config(state="disabled")

    def remove(self):
        for legitimate_attribute in self.legitimate_attributes:
            legitimate_attribute.remove()
        self.group_label.destroy()
        self.buttons_frame.destroy()

    def get(self):
        legitimate_attributes = list()
        for legitimate_attribute in self.legitimate_attributes:
            legitimate_attributes.append(legitimate_attribute.get())
        return " & ".join(legitimate_attributes)

    def disable(self):
        for legitimate_attribute in self.legitimate_attributes:
            legitimate_attribute.disable()
        self.add_button.config(state="disabled")
        self.remove_button.config(state="disabled")


class LegitimateAttribute:

    def __init__(self, frame, available_attributes, row, add_button_column, group_number):
        self.frame = frame
        self.available_attributes = available_attributes
        self.row = row
        self.add_button_column = add_button_column
        self.group_number = group_number
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
        self.current_attribute_values.grid(column=self.add_button_column - 1, row=self.row, padx=(0, 10), sticky="ew")

    def create_attributes_names_combobox(self):
        attributes_names = list(self.available_attributes.keys())
        attributes_names.sort()
        combobox = ttk.Combobox(self.frame, state="readonly", values=attributes_names, width=14, justify="center")
        combobox.current(0)
        combobox.grid(column=self.add_button_column - 3, row=self.row, pady=3)
        combobox.bind("<<ComboboxSelected>>", self.attribute_name_selected)
        return combobox

    def create_comparison_signs_combobox(self, comparison_signs):
        combobox = ttk.Combobox(self.frame, state="readonly", values=comparison_signs, width=4, justify="center")
        combobox.current(0)
        combobox.grid(column=self.add_button_column - 2, row=self.row, padx=2)
        return combobox

    def create_attribute_values_entry(self):
        text = tk.StringVar()
        text.set(0)
        validation_command = (self.frame.register(input_validator.validate_attribute_value_numeric))
        entry = ttk.Entry(self.frame, textvariable=text, width=17, justify="center", validate="key",
                          validatecommand=(validation_command, '%P'))
        return entry

    def create_attribute_values_combobox(self):
        attribute_name = self.attributes_names_combobox.get()
        attribute_values = list(self.available_attributes[attribute_name])
        combobox = ttk.Combobox(self.frame, state="readonly", values=attribute_values, width=14, justify="center")
        combobox.current(0)
        return combobox

    def attribute_name_selected(self, _):
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
            self.current_attribute_values.grid(column=self.add_button_column - 1, row=self.row, padx=(0, 10),
                                               sticky="ew")
        if not self.numeric_attribute:
            self.update_attribute_values_combobox()

    def update_comparison_signs_combobox(self, comparison_signs):
        self.comparison_signs_combobox["values"] = comparison_signs
        self.comparison_signs_combobox.current(0)

    def update_attribute_values_combobox(self):
        attribute_name = self.attributes_names_combobox.get()
        attribute_values = list(self.available_attributes[attribute_name])
        self.attribute_values_combobox["values"] = attribute_values
        self.attribute_values_combobox.current(0)

    def attribute_is_numeric(self, name):
        attribute_first_value = self.available_attributes[name][0]
        if not (isinstance(attribute_first_value, str)):
            return issubdtype(attribute_first_value, number)
        return False

    def disable(self):
        self.attributes_names_combobox.config(state="disabled")
        self.comparison_signs_combobox.config(state="disabled")
        self.attribute_values_entry.config(state="disabled")
        self.attribute_values_combobox.config(state="disabled")

    def enable(self):
        self.attributes_names_combobox.config(state="readonly")
        self.comparison_signs_combobox.config(state="readonly")
        self.attribute_values_entry.config(state="normal")
        self.attribute_values_combobox.config(state="readonly")

    def get_attribute_name(self):
        return self.attributes_names_combobox.get()

    def remove(self):
        self.attributes_names_combobox.destroy()
        self.comparison_signs_combobox.destroy()
        self.attribute_values_entry.destroy()
        self.attribute_values_combobox.destroy()

    def value_is_empty(self):
        empty = False
        if self.attribute_values_entry == self.current_attribute_values and len(self.attribute_values_entry.get()) == 0:
            empty = True
        return empty

    def get(self):
        name = self.attributes_names_combobox.get()
        if self.value_is_empty():
            raise ParameterNotDefined(ERROR_TITLE_GROUP.format(self.group_number, name),
                                      ERROR_DETAIL_GROUP.format(name))
        sign = self.comparison_signs_combobox.get()
        value = self.current_attribute_values.get()
        if self.attribute_values_combobox == self.current_attribute_values:
            string_template = "({}{}'{}')"
        else:
            string_template = "({}{}{})"
        return string_template.format(name, sign, value)
