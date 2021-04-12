from tkinter import ttk
from ttkthemes import ThemedTk

from dataset_handler import DatasetHandler
from user_interface.dataset_parameters import DatasetParameters
from user_interface.fairness_definitions_parameters import FairnessDefinitionsParameters

TOTAL_WIDTH = 1024
TOTAL_HEIGHT = 576


class GUI:

    def __init__(self, outcome_predictor):
        self.window = ThemedTk(theme='equilux')
        self.window.geometry("{}x{}".format(TOTAL_WIDTH, TOTAL_HEIGHT))

        dataset_parameters_frame = ttk.LabelFrame(self.window, text="Conjunto de datos", height=50,
                                                 width=TOTAL_WIDTH - 20)
        dataset_parameters_frame.grid(columnspan=11, column=0, row=0, padx=5, ipadx=5, pady=5)
        dataset_parameters_frame.grid_propagate(0)
        DatasetParameters(dataset_parameters_frame, outcome_predictor, self)

        self.fairness_definitions_frame = self.create_fairness_definitions_frame()
        self.fairness_definitions_parameters = None

        self.window.mainloop()

    def create_fairness_definitions_frame(self):
        fairness_definitions_frame = ttk.LabelFrame(self.window, text="Definiciones de fairness - parámetros",
                                                   height=100, width=TOTAL_WIDTH - 20)
        fairness_definitions_frame.grid(columnspan=11, column=0, row=1, padx=5, ipadx=5, pady=5)
        fairness_definitions_frame.grid_propagate(0)
        return fairness_definitions_frame

    def dataset_parameters_confirmed(self, filename, outcome_name, test_size):
        dataset_handler = DatasetHandler(filename, outcome_name, test_size)
        if self.fairness_definitions_parameters:
            self.fairness_definitions_frame.destroy()
            self.fairness_definitions_frame = self.create_fairness_definitions_frame()
        self.fairness_definitions_parameters = FairnessDefinitionsParameters(self.fairness_definitions_frame,
                                                                             dataset_handler)
