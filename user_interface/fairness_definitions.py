from tkinter import ttk
import tkinter as tk

from user_interface.images import Images


class FairnessDefinitionsContainer:

    def __init__(self, main_frame, width, calculate_callback):
        self.frame = ttk.LabelFrame(main_frame, text="  Definiciones de fairness - cálculo  ", height=300, width=width)
        self.fairness_definitions = None
        self.calculate_callback = calculate_callback

    def update(self, available_definitions, all_definitions):
        if self.fairness_definitions:
            self.fairness_definitions.destroy()
        self.fairness_definitions = \
            FairnessDefinitions(self.frame, available_definitions, all_definitions, self.calculate_callback)


class FairnessDefinitions:

    def __init__(self, frame, available_definitions, all_definitions, calculate_callback):
        self.calculate_callback = calculate_callback
        self.select_all_button = self.create_select_all_button(frame)
        self.unselect_all_button = self.create_unselect_all_button(frame)
        self.frame = ttk.Frame(frame)
        self.frame.grid(column=0, row=1, columnspan=3)
        self.images = Images()
        self.check_buttons = self.create_check_buttons(available_definitions, all_definitions)
        self.calculate_button = self.create_calculate_button(frame)

    def create_select_all_button(self, frame):
        select_all_button = ttk.Button(frame, text="Seleccionar todas", command=self.select_all)
        select_all_button.grid(column=0, row=0)
        return select_all_button

    def select_all(self):
        for (_, value, _) in self.check_buttons:
            value.set(True)

    def create_unselect_all_button(self, frame):
        unselect_all_button = ttk.Button(frame, text="Deseleccionar todas", command=self.unselect_all)
        unselect_all_button.grid(column=1, row=0)
        return unselect_all_button

    def unselect_all(self):
        for (_, value, _) in self.check_buttons:
            value.set(False)

    def create_check_buttons(self, available_definitions, all_definitions):
        check_buttons = list()
        all_definitions_names = list(all_definitions.keys())
        all_definitions_names.sort()
        for i, definition_name in enumerate(all_definitions_names):
            display_name = all_definitions[definition_name]
            value = tk.BooleanVar()
            value.set(False)
            if definition_name in available_definitions:
                frame = ttk.Frame(self.frame)
                image_label = ttk.Label(frame, image=self.images.question_mark)
                check_button = ttk.Checkbutton(frame, text=display_name, var=value)
                check_buttons.append((definition_name, value, image_label))
                frame.grid(column=0, row=i, sticky=tk.W)
                check_button.pack(side=tk.LEFT)
                image_label.pack(side=tk.LEFT)
            else:
                pass
                check_button = ttk.Checkbutton(self.frame, text="{} (no disponible)".format(display_name),
                                               var=value, state="disabled")
                check_button.grid(column=0, row=i, sticky=tk.W)
        return check_buttons

    def create_calculate_button(self, frame):
        calculate_button = ttk.Button(frame, text="Calcular", command=self.calculate)
        calculate_button.grid(column=2, row=2, sticky=tk.E)
        return calculate_button

    def calculate(self):
        selected_definitions = [name for (name, value, _) in self.check_buttons if value.get()]
        if len(selected_definitions) > 0:
            self.calculate_callback(selected_definitions)

    def destroy(self):
        self.select_all_button.destroy()
        self.unselect_all_button.destroy()
        self.calculate_button.destroy()
        self.frame.destroy()

    def show_result(self, result):
        for (definition_name, _, image_label) in self.check_buttons:
            if definition_name in result.keys():
                if result[definition_name].satisfies:
                    image = self.images.passed
                else:
                    image = self.images.failed
                image_label.configure(image=image)
