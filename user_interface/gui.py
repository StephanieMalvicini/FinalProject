import os
import tkinter as tk
from tkinter import ttk

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from fairness_definitions.fairness_definitions_calculator import FairnessDefinitionsCalculator
from handlers.dataset_handler import DatasetHandler
from handlers.decision_algorithm_handler import DecisionAlgorithmHandler
from handlers.outcome_handler import OutcomeHandler
from handlers.prediction_handler import PredictionHandler
from user_interface.dialogs import CustomDialog
from user_interface.dataset_parameters import DatasetParameters
from user_interface.decision_algorithm_parameters import DecisionAlgorithmParameters
from user_interface.fairness_definitions_parameters import FairnessDefinitionsParameters

TOTAL_WIDTH = 1100
TOTAL_HEIGHT = 600
FRAME_PADX = (20,20)
TOTAL_FRAME_PADX = 40
FRAME_PAXY = 5


class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.configure_window()
        self.style = self.configure_theme()
        self.canvas, self.main_frame = self.create_scrollbar()
        self.custom_dialog = self.create_custom_dialog()
        self.dataset_handler = None
        self.outcome_handler = OutcomeHandler()
        self.create_dataset_parameters_frame()
        self.decision_algorithm_name = None
        self.decision_algorithm = None
        self.decision_algorithm_handler = DecisionAlgorithmHandler()
        self.create_decision_algorithm_frame()
        self.fairness_definitions_parameters_frame = self.create_fairness_definitions_parameters_frame()
        self.fairness_definitions_calculator = None

        self.window.mainloop()

    def configure_window(self):
        self.window.title("Evaluador de fairness")
        self.window.iconbitmap("images/icon.ico")
        self.window.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))

    def configure_theme(self):
        style = ttk.Style(self.window)
        self.window.tk.eval("""
                set base_theme_dir {}/awthemes-10.3.0/

                package ifneeded awthemes 10.3.0 \
                    [list source [file join $base_theme_dir awthemes.tcl]]
                package ifneeded colorutils 4.8 \
                    [list source [file join $base_theme_dir colorutils.tcl]]
                package ifneeded awdark 7.11 \
                    [list source [file join $base_theme_dir awdark.tcl]]
                package ifneeded awlight 7.6 \
                    [list source [file join $base_theme_dir awlight.tcl]]
                """.format(os.getcwd().replace("\\", "/")))
        self.window.tk.call("package", "require", "awdark")
        self.window.tk.call("package", "require", "awlight")
        style.theme_use("awlight")
        self.window.configure(bg=style.lookup("TFrame", "background"))
        return style

    def create_scrollbar(self):
        # From: https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course
        bg = self.style.lookup("TFrame", "background")
        main_frame = tk.Frame(self.window, bg=bg)
        main_frame.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(main_frame, bg=bg, highlightthickness=0, relief="ridge")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', self.window_resized)
        second_frame = tk.Frame(canvas, bg=bg)
        second_frame.pack(fill=tk.BOTH, expand=1)
        canvas.create_window((0, 0), window=second_frame, anchor="nw", tags="frame")
        return canvas, second_frame

    def window_resized(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig("frame", height=self.canvas.winfo_height(), width=self.canvas.winfo_width())

    def create_custom_dialog(self):
        return CustomDialog(self.window, self.style)

    def create_dataset_parameters_frame(self):
        dataset_parameters_frame = ttk.LabelFrame(self.main_frame, text="  Conjunto de datos  ",
                                                  width=TOTAL_WIDTH - TOTAL_FRAME_PADX)
        dataset_parameters_frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        DatasetParameters(dataset_parameters_frame, self.outcome_handler, self.dataset_parameters_confirmed)

    def create_decision_algorithm_frame(self):
        decision_algorithm_frame = ttk.LabelFrame(self.main_frame, text="  Clasificador/Algoritmo de decisión  ",
                                                  width=TOTAL_WIDTH - TOTAL_FRAME_PADX)
        decision_algorithm_frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        decision_algorithms_names = self.decision_algorithm_handler.get_decision_algorithms_names()
        DecisionAlgorithmParameters(decision_algorithm_frame, decision_algorithms_names,
                                    self.decision_algorithm_parameters_confirmed)

    def create_fairness_definitions_parameters_frame(self):
        fairness_definitions_parameters_frame = ttk.LabelFrame(self.main_frame,
                                                               text="  Definiciones de fairness - parámetros  ",
                                                               height=150, width=TOTAL_WIDTH - TOTAL_FRAME_PADX)
        fairness_definitions_parameters_frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        return fairness_definitions_parameters_frame

    def dataset_parameters_confirmed(self, filename, outcome_name, test_size):
        self.dataset_handler = DatasetHandler(filename, outcome_name, test_size)
        if self.decision_algorithm_name:
            self.create_decision_algorithm()
        self.update_fairness_definitions()

    def decision_algorithm_parameters_confirmed(self, decision_algorithm_name):
        self.decision_algorithm_name = decision_algorithm_name
        if self.dataset_handler:
            self.create_decision_algorithm()
        self.update_fairness_definitions()

    def create_decision_algorithm(self):
        attributes_train, outcomes_train = self.dataset_handler.get_training_dataset()
        try:
            self.decision_algorithm = \
                self.decision_algorithm_handler.create_decision_algorithm(self.decision_algorithm_name,
                                                                          attributes_train,
                                                                          outcomes_train)
        except InvalidDecisionAlgorithmParameters as exception:
            self.custom_dialog.show_error(exception.message, exception.original_error)

    def update_fairness_definitions(self):
        if self.fairness_definitions_calculator:
            self.fairness_definitions_parameters_frame.destroy()
            self.fairness_definitions_parameters_frame = self.create_fairness_definitions_parameters_frame()
        if self.dataset_handler and self.decision_algorithm:
            attributes_test, _ = self.dataset_handler.get_testing_dataset()
            prediction_handler = PredictionHandler(self.decision_algorithm, attributes_test)
            try:
                self.fairness_definitions_calculator = FairnessDefinitionsCalculator(prediction_handler,
                                                                                     self.dataset_handler,
                                                                                     {},
                                                                                     self.outcome_handler)
                FairnessDefinitionsParameters(self.fairness_definitions_parameters_frame,
                                              self.dataset_handler,
                                              self.fairness_definitions_calculator.get_required_parameters_names())
            except InvalidDecisionAlgorithmParameters as exception:
                self.custom_dialog.show_error(exception.message, exception.original_error)
