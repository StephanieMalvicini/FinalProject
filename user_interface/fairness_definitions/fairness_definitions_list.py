import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from user_interface.images import FairnessDefinitionResultImages


class FairnessDefinitionsContainer:

    def __init__(self, main_frame, width, calculate_callback):
        self.frame = ttk.LabelFrame(main_frame, text="  Definiciones de fairness - cálculo  ", height=300, width=width)
        self.fairness_definitions = None
        self.calculate_callback = calculate_callback

    def update(self, testing_set_downloader, all_definitions, available_definitions_names):
        if self.fairness_definitions:
            self.fairness_definitions.destroy()
        self.fairness_definitions = FairnessDefinitionsList(self.frame, self.calculate_callback, testing_set_downloader,
                                                            all_definitions, available_definitions_names)

    def show_result(self, results, plots):
        self.fairness_definitions.show_result(results, plots)


class FairnessDefinitionsList:

    def __init__(self, parent_frame, calculate_callback, testing_set_downloader, all_definitions,
                 available_definitions_names):
        self.buttons_frame = ttk.Frame(parent_frame)
        self.buttons_frame.pack(fill=tk.X, anchor=tk.NW, padx=10, pady=(7, 3))
        self.testing_set_downloader = testing_set_downloader
        self.create_select_all_button()
        self.create_unselect_all_button()
        self.basic_metrics_plot_button, self.tables_plot_button = self.create_plots_buttons()
        self.create_testing_set_button()
        self.create_calculate_button(calculate_callback)
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(anchor=tk.W, fill=tk.X, padx=10, pady=(5, 10))
        self.fairness_definitions_items = self.create_check_buttons(all_definitions, available_definitions_names)

    def create_select_all_button(self):
        button = ttk.Button(self.buttons_frame, text="Seleccionar todas", width=20, command=self.select_all)
        button.pack(side=tk.LEFT, anchor=tk.NW, padx=(0, 10))
        return button

    def select_all(self):
        for definition in self.fairness_definitions_items:
            definition.value.set(True)

    def create_unselect_all_button(self):
        button = ttk.Button(self.buttons_frame, text="Deseleccionar todas", width=20,
                            command=self.unselect_all)
        button.pack(side=tk.LEFT, anchor=tk.NW)
        return button

    def unselect_all(self):
        for definition in self.fairness_definitions_items:
            definition.value.set(False)

    def create_plots_buttons(self):
        basic_metrics_button = ttk.Button(self.buttons_frame, text="Ver métricas básicas", state="disabled")
        basic_metrics_button.pack(side=tk.RIGHT, anchor=tk.NE)
        tables_button = ttk.Button(self.buttons_frame, text="Ver cantidades probabilidad", state="disabled")
        tables_button.pack(side=tk.RIGHT, anchor=tk.NE, padx=2)
        return basic_metrics_button, tables_button

    def create_testing_set_button(self):
        button = ttk.Button(self.buttons_frame, text="Descargar conjunto de pruebas",
                            command=self.open_filename_selector)
        button.pack(side=tk.RIGHT, anchor=tk.NE)

    def open_filename_selector(self):
        filename = filedialog.asksaveasfilename(title="Guardar como", filetypes=(("CSV Files", "*.csv"),),
                                                defaultextension=".csv")
        if filename:
            self.testing_set_downloader.download_dataset(filename)

    def create_calculate_button(self, callback):
        button = ttk.Button(self.buttons_frame, text="Calcular", width=10, command=lambda: self.calculate(callback))
        button.pack(side=tk.RIGHT, anchor=tk.NE, padx=(0, 5))
        return button

    def calculate(self, callback):
        selected_definitions = [item.definition_name for item in self.fairness_definitions_items if item.is_selected()]
        if len(selected_definitions) > 0:
            callback(selected_definitions)

    def create_check_buttons(self, all_definitions, available_definitions_names):
        check_buttons = list()
        for definition in all_definitions:
            value = tk.BooleanVar()
            value.set(False)
            if definition.name in available_definitions_names:
                check_buttons.append(
                    FairnessDefinition(definition, self.frame, value))
            else:
                check_button = ttk.Checkbutton(self.frame, text="{} (no disponible)".format(definition.display_name),
                                               var=value, state="disabled")
                check_button.pack(anchor=tk.W, fill=tk.X, pady=(2, 0))
        return check_buttons

    def destroy(self):
        self.buttons_frame.destroy()
        self.frame.destroy()

    def show_result(self, results, plots):
        self.configure_plots(plots)
        for item in self.fairness_definitions_items:
            if item.definition_name in results.keys():
                item.add_result(results[item.definition_name])

    def configure_plots(self, plots):
        if plots.has_basic_metrics_plot():
            self.basic_metrics_plot_button.config(command=plots.show_basic_metrics, state="normal")
        if plots.has_positives_negatives_tables_plot():
            self.tables_plot_button.config(command=plots.show_positives_negatives_tables, state="normal")


class FairnessDefinition:

    def __init__(self, definition, parent_frame, value):
        self.definition_name = definition.name
        self.value = value
        self.images = FairnessDefinitionResultImages()
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(anchor=tk.W, fill=tk.X)
        self.image_label, self.name_and_icon_frame = self.create_name_and_icon(definition.display_name)
        self.show_more_button = self.create_show_more_button()
        self.result_frame = ttk.Frame(self.frame)

    def create_name_and_icon(self, display_name):
        name_and_icon_frame = ttk.Frame(self.frame)
        name_and_icon_frame.pack(anchor=tk.W)
        image_label = ttk.Label(name_and_icon_frame, image=self.images.question_mark)
        check_button = ttk.Checkbutton(name_and_icon_frame, text=display_name, var=self.value)
        check_button.pack(side=tk.LEFT, pady=(2, 0))
        image_label.pack(side=tk.LEFT, padx=2)
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

    def is_selected(self):
        return self.value.get()
