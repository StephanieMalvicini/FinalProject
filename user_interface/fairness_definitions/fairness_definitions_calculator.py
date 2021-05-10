import tkinter as tk
from tkinter import ttk

from exceptions.decision_algorithm import InvalidDecisionAlgorithmParameters, InvalidModuleName
from exceptions.parameters import ParameterNotDefined
from handlers import decision_algorithm_creator
from handlers.dataset_handler import DatasetHandler
from handlers.descriptions_calculator import get_descriptions
from handlers.fairness_definitions_calculator import FairnessDefinitionsCalculator
from handlers.fairness_definitions_parameters_handler import FairnessDefinitionsParametersHandler
from handlers.prediction_handler import PredictionHandler
from user_interface.fairness_definitions.descriptions import DescriptionsContainer
from user_interface.fairness_definitions.dataset_parameters import DatasetParametersContainer
from user_interface.fairness_definitions.fairness_definitions_list import FairnessDefinitionsContainer
from user_interface.fairness_definitions.fairness_definitions_parameters import FairnessDefinitionsParametersContainer
from user_interface.plots import Plots

FRAME_PADX = (20, 20)
TOTAL_FRAME_PADX = 40
FRAME_PAXY = 5

UNEXPECTED_ERROR_TITLE = "Error inesperado"


class FairnessDefinitionsCalculatorUI:

    def __init__(self, total_width, dialog, main_frame):
        self.dialog = dialog
        self.frame = ttk.Frame(main_frame)
        self.frame.pack(fill=tk.X)

        self.dataset_handler = None
        self.prediction_handler = None
        self.parameters_handler = None
        self.last_used_values = \
            {"filename": None, "outcome_name": None, "test_size": None, "decision_algorithm_name": None}
        self.calculator = None

        width = total_width - TOTAL_FRAME_PADX
        self.dataset_parameters = \
            DatasetParametersContainer(self.frame, width, self.dataset_parameters_confirmed, self.dialog)
        self.descriptions = \
            DescriptionsContainer(self.frame, width)
        self.parameters = \
            FairnessDefinitionsParametersContainer(self.frame, width, self.dialog)
        self.definitions = FairnessDefinitionsContainer(self.frame, width, self.calculate, self.dialog)
        self.pack_containers()

    def pack_containers(self):
        self.dataset_parameters.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.descriptions.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.parameters.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.definitions.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)

    def dataset_parameters_confirmed(self, filename, outcome_name, test_size, decision_algorithm_name):
        try:
            if self.update_handlers(filename, outcome_name, test_size, decision_algorithm_name):
                self.descriptions.update(self.dataset_handler.get_attributes_values())
                required_parameters_names = self.parameters_handler.get_all_required_parameters_names()
                self.parameters.update(self.dataset_handler, required_parameters_names)
                available_definitions = self.parameters_handler.get_available_definitions_names()
                all_definitions_display_names = self.parameters_handler.get_all_definitions_displays_names()
                self.definitions.update(available_definitions, all_definitions_display_names,
                                        self.dataset_handler.get_testing_set_to_show())
        except InvalidDecisionAlgorithmParameters as exception:
            self.dialog.show_error_with_details(exception.message, exception.original_error)

    def update_handlers(self, filename, outcome_name, test_size, decision_algorithm_name):
        updated = False
        dataset_handler = self.dataset_handler
        if self.last_used_values["filename"] != filename or self.last_used_values["outcome_name"] != outcome_name or \
                self.last_used_values["test_size"] != test_size:
            dataset_handler = DatasetHandler(filename, outcome_name, test_size)
            updated = True
        if self.last_used_values["decision_algorithm_name"] != decision_algorithm_name or updated:
            training_data = dataset_handler.get_training_dataset()
            try:
                decision_algorithm = decision_algorithm_creator.get(decision_algorithm_name, *training_data)
                updated = True
            except InvalidDecisionAlgorithmParameters as exception:
                self.dialog.show_error_with_details(exception.message, exception.original_error)
                return False
            except InvalidModuleName as exception:
                self.dialog.show_error(exception.title, exception.message)
                return False
        else:
            decision_algorithm = self.prediction_handler.decision_algorithm
        if updated:
            attributes_test, _ = dataset_handler.get_testing_dataset()
            self.prediction_handler = PredictionHandler(decision_algorithm, attributes_test)
            self.parameters_handler = \
                FairnessDefinitionsParametersHandler(self.prediction_handler, dataset_handler)
            self.calculator = None
        self.last_used_values = {"filename": filename, "outcome_name": outcome_name, "test_size": test_size,
                                 "decision_algorithm_name": decision_algorithm_name}
        self.dataset_handler = dataset_handler
        return updated

    def calculate(self, selected_definitions):
        try:
            descriptions = get_descriptions(self.descriptions.descriptions.get_descriptions())
            required_parameters = self.parameters_handler.get_required_parameters_names(selected_definitions)
            parameters_values = self.parameters.get_parameters_values(required_parameters)
            self.parameters_handler.transform_parameters_type(parameters_values)
            if not self.calculator:
                self.calculator = FairnessDefinitionsCalculator(self.dataset_handler, self.prediction_handler,
                                                                self.dataset_parameters.outcome_handler)
            self.calculator.update_parameters(descriptions, parameters_values)
            parameters_display_names = self.parameters_handler.get_all_parameters_display_names()
            result = self.calculator.calculate(selected_definitions, parameters_display_names)
            tables = self.calculator.get_positives_negatives_table()
            plots = Plots(self.dialog, descriptions, self.calculator.get_basic_metrics(), tables[0], tables[1])
            self.definitions.show_result(result, plots)
        except ParameterNotDefined as e:
            self.dialog.show_error(e.error_title, e.message)
        except InvalidDecisionAlgorithmParameters as e:
            self.dialog.show_error_with_details(e.message, e.original_error)
        # except Exception:
        #    self.dialog.show_error_with_details(UNEXPECTED_ERROR_TITLE, sys.exc_info())

    def destroy(self):
        self.frame.destroy()
