import tkinter as tk
from tkinter import ttk

from databases import fairness_definitions, parameters
from exceptions.decision_algorithm import InvalidDecisionAlgorithmParameters, InvalidModuleName
from exceptions.parameters import ParameterNotDefined
from handlers import decision_algorithm_creator, parameter_converter
from handlers.dataset_downloader import DatasetDownloader
from handlers.dataset_handler import DatasetHandler
from handlers import descriptions_calculator
from handlers.fairness_definitions_calculator import FairnessDefinitionsCalculator
from handlers.decision_algorithm_adapter import DecisionAlgorithmAdapter
from user_interface.fairness_definitions_window.descriptions import DescriptionsContainer
from user_interface.fairness_definitions_window.dataset_parameters import DatasetParametersContainer
from user_interface.fairness_definitions_window.fairness_definitions_list import FairnessDefinitionsContainer
from user_interface.fairness_definitions_window.parameters import FairnessDefinitionsParametersContainer
from user_interface.plots import Plots

FRAME_PADX = (20, 20)
TOTAL_FRAME_PADX = 40
FRAME_PAXY = 5

UNEXPECTED_ERROR_TITLE = "Error inesperado"


class LastUsedValues:

    def __init__(self, filename=None, outcome_name=None, test_size=None, decision_algorithm_name=None):
        self.filename = filename
        self.outcome_name = outcome_name
        self.test_size = test_size
        self.decision_algorithm_name = decision_algorithm_name


class FairnessDefinitionsCalculatorUI:

    def __init__(self, total_width, dialog, main_frame):
        self.dialog = dialog
        self.frame = ttk.Frame(main_frame)
        self.frame.pack(fill=tk.X)

        self.dataset_handler = None
        self.prediction_handler = None
        self.last_used_values = LastUsedValues()
        self.calculator = None

        width = total_width - TOTAL_FRAME_PADX
        self.dataset_parameters = \
            DatasetParametersContainer(self.frame, width, self.update_containers, self.dialog)
        self.descriptions = \
            DescriptionsContainer(self.frame, width)
        self.parameters = \
            FairnessDefinitionsParametersContainer(self.frame, width, self.dialog)
        self.definitions = FairnessDefinitionsContainer(self.frame, width, self.calculate)
        self.pack_containers()

    def pack_containers(self):
        self.dataset_parameters.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.descriptions.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.parameters.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.definitions.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)

    def update_containers(self, filename, outcome_name, test_size, decision_algorithm_name):
        try:
            if self.update_handlers(filename, outcome_name, test_size, decision_algorithm_name):
                self.descriptions.update(self.dataset_handler.get_attributes_values())
                all_definitions = fairness_definitions.get_all()
                available_definitions_names = \
                    fairness_definitions.get_available_names(self.dataset_handler.has_outcome(),
                                                             self.prediction_handler.predicted_outcome_available(),
                                                             self.prediction_handler.predicted_probability_available(),
                                                             self.prediction_handler.distances_available())
                testing_set_downloader = DatasetDownloader(self.dataset_handler.get_testing_set_to_show())
                self.definitions.update(testing_set_downloader,
                                        all_definitions, available_definitions_names)
                required_parameters_names = parameters.get_required_names(available_definitions_names)
                all_parameters = parameters.get_all()
                attributes_values = self.dataset_handler.get_attributes_values()
                self.parameters.update(attributes_values, required_parameters_names, all_parameters)
        except InvalidDecisionAlgorithmParameters as exception:
            self.dialog.show_error_with_details(exception.message, exception.original_error)

    def update_handlers(self, filename, outcome_name, test_size, decision_algorithm_name):
        updated = False
        dataset_handler = self.dataset_handler
        if self.last_used_values.filename != filename or self.last_used_values.outcome_name != outcome_name or \
                self.last_used_values.test_size != test_size:
            dataset_handler = DatasetHandler(filename, outcome_name, test_size)
            updated = True
        if self.last_used_values.decision_algorithm_name != decision_algorithm_name or updated:
            training_data = dataset_handler.get_training_dataset()
            try:
                decision_algorithm = decision_algorithm_creator.get(decision_algorithm_name, training_data)
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
            self.prediction_handler = DecisionAlgorithmAdapter(decision_algorithm, attributes_test)
            self.calculator = None
        self.last_used_values = LastUsedValues(filename, outcome_name, test_size, decision_algorithm_name)
        self.dataset_handler = dataset_handler
        return updated

    def calculate(self, selected_definitions_names):
        try:
            descriptions = descriptions_calculator.get(self.descriptions.get_selected())
            required_parameters_names = parameters.get_required_names(selected_definitions_names)
            parameters_values = self.parameters.get_parameters_values(required_parameters_names)
            parameter_converter.transform_parameters_type(parameters_values)
            if not self.calculator:
                self.calculator = FairnessDefinitionsCalculator(self.dataset_handler, self.prediction_handler,
                                                                *self.dataset_parameters.get_outcome_data())
            self.calculator.update_parameters(descriptions, parameters_values)
            result = self.calculator.calculate(selected_definitions_names)
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
