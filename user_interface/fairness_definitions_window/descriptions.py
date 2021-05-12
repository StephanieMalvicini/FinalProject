from tkinter import ttk
import tkinter as tk

from exceptions.parameters import ParameterNotDefined

CONTAINER_NAME = "  Atributos descripciones  "
AMOUNT_PER_ROW = 6
ERROR_TITLE = "Ningún atributo para las descripciones seleccionado"
ERROR_DETAIL = "Por favor selecciona al menos un atributo antes de confirmar"


class DescriptionsContainer:

    def __init__(self, main_frame, width):
        self.frame = ttk.LabelFrame(main_frame, text=CONTAINER_NAME, height=100, width=width)
        self.descriptions = None

    def update(self, attributes_values):
        if self.descriptions:
            self.descriptions.destroy()
        self.descriptions = Descriptions(self.frame, attributes_values)

    def get_selected(self):
        return self.descriptions.get_descriptions()


class Descriptions:

    def __init__(self, frame, attributes_values):
        self.frame = ttk.Frame(frame)
        self.frame.pack(fill=tk.X, pady=(7, 10))
        self.attributes_values = attributes_values
        self.row = 0
        self.check_buttons = self.create_check_buttons()

    def create_check_buttons(self):
        check_buttons = list()
        column = 0
        attributes_names = list(self.attributes_values.keys())
        attributes_names.sort()
        for i, name in enumerate(attributes_names):
            value = tk.BooleanVar()
            value.set(False)
            check_button = ttk.Checkbutton(self.frame, text=name, var=value, width=29)
            if i % AMOUNT_PER_ROW == 0:
                column = 0
                self.row += 1
            else:
                column += 1
            check_button.grid(column=column, row=self.row, padx=(10, 0))
            check_buttons.append((name, value))
        return check_buttons

    def get_descriptions(self):
        attributes_checked = [name for (name, value) in self.check_buttons if value.get()]
        if len(attributes_checked) == 0:
            raise ParameterNotDefined(ERROR_TITLE, ERROR_DETAIL)
        else:
            attributes_values = {name: self.attributes_values[name] for name in attributes_checked}
            return attributes_values

    def destroy(self):
        self.frame.destroy()
