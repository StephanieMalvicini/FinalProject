import sys
from tkinter import ttk

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from exceptions.parameter_not_defined import ParameterNotDefined
from handlers.dataset_handler import DatasetHandler
from handlers.descriptions_calculator import get_descriptions
from handlers.fairness_definitions_calculator import calculate
from handlers.fairness_definitions_parameters_handler import FairnessDefinitionsParametersHandler
from handlers.prediction_handler import PredictionHandler
from user_interface.descriptions import DescriptionsContainer
from user_interface.dataset_parameters import DatasetParametersContainer
from user_interface.fairness_definitions import FairnessDefinitionsContainer
from user_interface.fairness_definitions_parameters import FairnessDefinitionsParametersContainer

FRAME_PADX = (20, 20)
TOTAL_FRAME_PADX = 40
FRAME_PAXY = 5

UNEXPECTED_ERROR_TITLE = "Error inesperado"


class FairnessDefinitionsCalculator:

    def __init__(self, total_width, dialog, main_frame):
        self.dialog = dialog
        self.frame = ttk.Frame(main_frame)
        self.frame.pack()

        self.dataset_handler = None
        self.prediction_handler = None
        self.fairness_definitions_parameters_handler = None
        self.last_used_values = \
            {"filename": None, "outcome_name": None, "test_size": None, "decision_algorithm_name": None}

        width = total_width - TOTAL_FRAME_PADX
        self.dataset_parameters_container = \
            DatasetParametersContainer(self.frame, width, self.dataset_parameters_confirmed, self.dialog)
        self.descriptions_container = \
            DescriptionsContainer(self.frame, width)
        self.fairness_definitions_parameters_container = \
            FairnessDefinitionsParametersContainer(self.frame, width, self.dialog)
        self.fairness_definitions_container = FairnessDefinitionsContainer(self.frame, width, self.calculate)
        self.pack_containers()

    def pack_containers(self):
        self.dataset_parameters_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.descriptions_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.fairness_definitions_parameters_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.fairness_definitions_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)

    def dataset_parameters_confirmed(self, filename, outcome_name, test_size, decision_algorithm_name):
        try:
            if self.update_handlers(filename, outcome_name, test_size, decision_algorithm_name):
                self.descriptions_container.update(self.dataset_handler.get_attributes_values())
                required_parameters_names = self.fairness_definitions_parameters_handler.get_required_parameters_names()
                available_definitions = self.fairness_definitions_parameters_handler.get_available_definitions_names()
                all_definitions = self.fairness_definitions_parameters_handler.get_all_definitions_names()
                self.fairness_definitions_parameters_container.update(self.dataset_handler, required_parameters_names)
                self.fairness_definitions_container.update(available_definitions, all_definitions)
        except InvalidDecisionAlgorithmParameters as exception:
            self.dialog.show_error_with_details(exception.message, exception.original_error)

    def update_handlers(self, filename, outcome_name, test_size, decision_algorithm_name):
        updated = False
        if self.last_used_values["filename"] != filename or \
                self.last_used_values["outcome_name"] != outcome_name or \
                self.last_used_values["test_size"] != test_size:
            try:
                self.dataset_handler = DatasetHandler(filename, outcome_name, test_size)
                updated = True
                if self.last_used_values["decision_algorithm_name"] != decision_algorithm_name or updated:
                    attributes, outcomes = self.dataset_handler.get_training_dataset()
                    decision_algorithm = self.dataset_parameters_container.decision_algorithm_handler. \
                        create_decision_algorithm(decision_algorithm_name, attributes, outcomes)
                    updated = True
                else:
                    decision_algorithm = self.prediction_handler.decision_algorithm
                if updated:
                    attributes_test, _ = self.dataset_handler.get_testing_dataset()
                    self.prediction_handler = PredictionHandler(decision_algorithm, attributes_test)
                    self.fairness_definitions_parameters_handler = \
                        FairnessDefinitionsParametersHandler(self.prediction_handler, self.dataset_handler)
                self.last_used_values = {"filename": filename, "outcome_name": outcome_name, "test_size": test_size,
                                         "decision_algorithm_name": decision_algorithm_name}
            except Exception:
                self.dialog.show_error_with_details(UNEXPECTED_ERROR_TITLE, sys.exc_info())
        return updated

    def calculate(self, selected_definitions):
        try:
            descriptions = get_descriptions(self.descriptions_container.descriptions.get_descriptions())
            parameters_values = \
                self.fairness_definitions_parameters_container.fairness_definitions_parameters.get_parameters_values()
            self.fairness_definitions_parameters_handler.transform_parameters_type(parameters_values)
            result = calculate(selected_definitions, descriptions, parameters_values, self.dataset_handler,
                               self.prediction_handler, self.dataset_parameters_container.outcome_handler)
            self.fairness_definitions_container.fairness_definitions.show_result(result)
        except ParameterNotDefined as e:
            self.dialog.show_error(e.error_title, e.message)
        # except InvalidDecisionAlgorithmParameters as e:
        #    self.dialog.show_error_with_details(e.message, e.original_error)

    def destroy(self):
        self.frame.destroy()