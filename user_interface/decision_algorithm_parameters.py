from tkinter import ttk


class DecisionAlgorithmParameters:

    def __init__(self, frame, decision_algorithms, confirmed_callback):
        self.frame = frame
        self.decision_algorithms = decision_algorithms
        self.decision_algorithms.sort()
        self.confirmed_callback = confirmed_callback
        self.decision_algorithm_combobox = self.create_decision_algorithm_combobox()
        self.confirm_button = self.create_confirm_button()

    def create_decision_algorithm_combobox(self):
        decision_algorithm_name_label = ttk.Label(self.frame, text="Nombre: ")
        decision_algorithm_name_label.grid(column=0, row=0)
        decision_algorithm_combobox = ttk.Combobox(self.frame, state="readonly", values=self.decision_algorithms)
        decision_algorithm_combobox.current(0)
        decision_algorithm_combobox.grid(column=1, row=0)
        return decision_algorithm_combobox

    def create_confirm_button(self):
        confirm_button = ttk.Button(self.frame, text="Confirmar", command=self.decision_algorithm_parameters_confirmed)
        confirm_button.grid(column=12, row=0)
        confirm_button.grid_propagate(0)
        return confirm_button

    def decision_algorithm_parameters_confirmed(self):
        decision_algorithm = self.decision_algorithm_combobox.get()
        self.confirmed_callback(decision_algorithm)
