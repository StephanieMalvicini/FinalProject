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

    def __init__(self, parent_frame, available_definitions, all_definitions, calculate_callback):
        self.calculate_callback = calculate_callback
        buttons_frame = ttk.Frame(parent_frame)
        buttons_frame.pack(fill=tk.X, anchor=tk.NW)
        self.select_all_button = self.create_select_all_button(buttons_frame)
        self.unselect_all_button = self.create_unselect_all_button(buttons_frame)
        self.calculate_button = self.create_calculate_button(buttons_frame)
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(anchor=tk.W, fill=tk.X)
        self.fairness_definitions = self.create_check_buttons(available_definitions, all_definitions)

    def create_select_all_button(self, buttons_frame):
        select_all_button = ttk.Button(buttons_frame, text="Seleccionar todas", command=self.select_all)
        select_all_button.pack(side=tk.LEFT, anchor=tk.NW)
        return select_all_button

    def select_all(self):
        for definition in self.fairness_definitions:
            definition.value.set(True)

    def create_unselect_all_button(self, buttons_frame):
        unselect_all_button = ttk.Button(buttons_frame, text="Deseleccionar todas", command=self.unselect_all)
        unselect_all_button.pack(side=tk.LEFT, anchor=tk.NW)
        return unselect_all_button

    def unselect_all(self):
        for definition in self.fairness_definitions:
            definition.value.set(False)

    def create_calculate_button(self, buttons_frame):
        calculate_button = ttk.Button(buttons_frame, text="Calcular", command=self.calculate)
        calculate_button.pack(side=tk.RIGHT, anchor=tk.NE)
        return calculate_button

    def calculate(self):
        selected_definitions = [definition.name for definition in self.fairness_definitions if definition.value.get()]
        if len(selected_definitions) > 0:
            self.calculate_callback(selected_definitions)

    def create_check_buttons(self, available_definitions, all_definitions):
        fairness_definitions = list()
        all_definitions_names = list(all_definitions.keys())
        all_definitions_names.sort()
        for definition_name in all_definitions_names:
            display_name = all_definitions[definition_name]
            value = tk.BooleanVar()
            value.set(False)
            if definition_name in available_definitions:
                fairness_definitions.append(
                    FairnessDefinition(definition_name, display_name, self.frame, value))
            else:
                check_button = ttk.Checkbutton(self.frame, text="{} (no disponible)".format(display_name),
                                               var=value, state="disabled")
                check_button.pack(anchor=tk.W, fill=tk.X)
        return fairness_definitions

    def destroy(self):
        self.select_all_button.destroy()
        self.unselect_all_button.destroy()
        self.calculate_button.destroy()
        self.frame.destroy()

    def show_result(self, results):
        for definition in self.fairness_definitions:
            if definition.name in results.keys():
                definition.add_result(results[definition.name])


class FairnessDefinition:

    def __init__(self, definition_name, display_name, parent_frame, value):
        self.name = definition_name
        self.value = value
        self.images = Images()
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(anchor=tk.W, fill=tk.X)
        self.image_label, self.name_and_icon_frame = self.create_name_and_icon(display_name)
        self.show_more_button = self.create_show_more_button()
        self.result_frame = ttk.Frame(self.frame)
        self.has_result = False

    def create_name_and_icon(self, display_name):
        name_and_icon_frame = ttk.Frame(self.frame)
        name_and_icon_frame.pack(anchor=tk.W)
        image_label = ttk.Label(name_and_icon_frame, image=self.images.question_mark)
        check_button = ttk.Checkbutton(name_and_icon_frame, text=display_name, var=self.value)
        check_button.pack(side=tk.LEFT)
        image_label.pack(side=tk.LEFT)
        return image_label, name_and_icon_frame

    def create_show_more_button(self):
        show_more_button = tk.Button(self.name_and_icon_frame, command=self.show_more, image=self.images.show_more,
                                     highlightthickness=0, bd=0, state="disabled")
        show_more_button.pack(side=tk.LEFT)
        return show_more_button

    def show_more(self):
        self.result_frame.pack(anchor=tk.W)
        self.show_more_button.config(command=self.show_less, image=self.images.show_less)

    def show_less(self):
        self.result_frame.pack_forget()
        self.show_more_button.config(command=self.show_more, image=self.images.show_more)

    def add_result(self, result):
        if self.has_result:
            separator = ttk.Separator(self.result_frame, orient='horizontal')
            separator.pack(fill=tk.X)
        else:
            self.has_result = True
        self.change_icon(result.satisfies)
        self.show_more_button.config(state="normal")
        new_result_frame = ttk.Frame(self.result_frame)
        new_result_frame.pack(anchor=tk.W, padx=5, pady=5)
        result.show(new_result_frame)

    def change_icon(self, passed):
        if passed:
            image = self.images.passed
        else:
            image = self.images.failed
        self.image_label.configure(image=image)
