import tkinter as tk
from user_interface.dataset_parameters import DatasetParameters
from user_interface.fairness_definitions import FairnessDefinitions


class GUI:

    def __init__(self, outcome_predictor):
        self.window = tk.Tk()

        self.dataset_parameters_frame = tk.Frame(self.window)
        self.dataset_parameters_frame.grid(column=0, row=0)
        self.dataset_parameters = DatasetParameters(self.dataset_parameters_frame, outcome_predictor, self)

        self.fairness_definitions_frame = tk.Frame(self.window)
        self.fairness_definitions_frame.grid(column=0, row=1)
        self.fairness_definitions_frame = FairnessDefinitions(self.fairness_definitions_frame)

        self.window.mainloop()

    def dataset_parameters_continue_button_pressed(self):
        self.fairness_definitions_frame.show()
