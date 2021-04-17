from tkinter import ttk
import tkinter as tk


class FairnessDefinitionsContainer:

    def __init__(self, main_frame, width):
        self.frame = ttk.LabelFrame(main_frame, text="  Definiciones de fairness - cálculo  ", height=300, width=width)
        self.fairness_definitions = None

    def update(self, fairness_definitions_parameters_handler):
        if self.fairness_definitions:
            self.fairness_definitions.destroy()
        self.fairness_definitions = FairnessDefinitions(self.frame, fairness_definitions_parameters_handler)


class FairnessDefinitions:

    def __init__(self, frame, fairness_definitions_parameters_handler):
        self.frame = ttk.Frame(frame)
        self.frame.grid(column=0, row=0)
        self.fairness_definitions_parameters_handler = fairness_definitions_parameters_handler
        self.select_all_button = self.create_select_all_button()
        self.unselect_all_button = self.create_unselect_all_button()
        self.check_buttons = self.create_check_buttons()

    def create_select_all_button(self):
        select_all_button = ttk.Button(self.frame, text="Seleccionar todas", command=self.select_all)
        select_all_button.grid(column=0, row=0)
        return select_all_button

    def select_all(self):
        for (_, value) in self.check_buttons:
            value.set(True)

    def create_unselect_all_button(self):
        unselect_all_button = ttk.Button(self.frame, text="Deseleccionar todas", command=self.unselect_all)
        unselect_all_button.grid(column=1, row=0)
        return unselect_all_button

    def unselect_all(self):
        for (_, value) in self.check_buttons:
            value.set(False)

    def create_check_buttons(self):
        check_buttons = list()
        available_fairness_definitions = self.fairness_definitions_parameters_handler.get_available_definitions_names()
        fairness_definitions = self.fairness_definitions_parameters_handler.get_all_definitions_names()
        fairness_definitions.sort()
        for i, definition_name in enumerate(fairness_definitions):
            value = tk.BooleanVar()
            value.set(False)
            if definition_name in available_fairness_definitions:
                check_button = ttk.Checkbutton(self.frame, text=definition_name, var=value)
                check_buttons.append((definition_name, value))
            else:
                check_button = ttk.Checkbutton(self.frame, text="{} (no disponible)".format(definition_name),
                                               var=value, state="disabled")
            check_button.grid(sticky=tk.W, column=0, row=i+1, columnspan=12)
        return check_buttons

    def destroy(self):
        self.frame.destroy()
