from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from handlers.dataset_handler import DatasetHandler
from handlers.descriptions_calculator import get_descriptions
from handlers.fairness_definitions_parameters_handler import FairnessDefinitionsParametersHandler
from handlers.prediction_handler import PredictionHandler
from user_interface.descriptions import DescriptionsContainer
from user_interface.dataset_parameters import DatasetParametersContainer
from user_interface.fairness_definitions import FairnessDefinitionsContainer
from user_interface.fairness_definitions_parameters import FairnessDefinitionsParametersContainer
from user_interface.custom_window import CustomWindow

TOTAL_WIDTH = 1300
TOTAL_HEIGHT = 600
FRAME_PADX = (20,20)
TOTAL_FRAME_PADX = 40
FRAME_PAXY = 5


class GUI:

    def __init__(self):
        custom_window = CustomWindow(TOTAL_WIDTH, TOTAL_HEIGHT)
        main_frame = custom_window.main_frame
        self.dialog = custom_window.dialog

        width = TOTAL_WIDTH - TOTAL_FRAME_PADX
        self.dataset_parameters_container = \
            DatasetParametersContainer(main_frame, width, self.dataset_parameters_confirmed, self.dialog)
        self.descriptions_container = \
            DescriptionsContainer(main_frame, width)
        self.fairness_definitions_parameters_container = \
            FairnessDefinitionsParametersContainer(main_frame, width, self.dialog)
        self.fairness_definitions_container = FairnessDefinitionsContainer(main_frame, width)
        self.pack_containers()

        custom_window.window.mainloop()

    def pack_containers(self):
        self.dataset_parameters_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.descriptions_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.fairness_definitions_parameters_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)
        self.fairness_definitions_container.frame.pack(fill='x', padx=FRAME_PADX, pady=FRAME_PAXY)

    def dataset_parameters_confirmed(self, filename, outcome_name, test_size, decision_algorithm_name):
        try:
            dataset_handler = DatasetHandler(filename, outcome_name, test_size)
            attributes, outcomes = dataset_handler.get_training_dataset()
            decision_algorithm = self.dataset_parameters_container.decision_algorithm_handler.\
                create_decision_algorithm(decision_algorithm_name, attributes, outcomes)
            attributes_test, _ = dataset_handler.get_testing_dataset()
            prediction_handler = PredictionHandler(decision_algorithm, attributes_test)
            fairness_definitions_parameters_handler = \
                FairnessDefinitionsParametersHandler(prediction_handler, dataset_handler)
            self.descriptions_container.update(dataset_handler.get_attributes_values())
            self.fairness_definitions_parameters_container.\
                update(dataset_handler, fairness_definitions_parameters_handler)
            self.fairness_definitions_container.update(fairness_definitions_parameters_handler)
        except InvalidDecisionAlgorithmParameters as exception:
            self.dialog.show_error_with_details(exception.message, exception.original_error)

    def descriptions_confirmed(self, attributes_checked):
        self.descriptions = get_descriptions(attributes_checked)
