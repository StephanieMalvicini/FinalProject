import sys

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from fairness_definitions.discrimination_basics import calculate_basic_metrics, \
    create_positives_negatives_tables, create_probabilities_table


def get_testing_set(dataset_handler, prediction_handler):
    try:
        attributes_test, outcomes_test = dataset_handler.get_testing_dataset()
        if dataset_handler.has_outcome():
            attributes_test["Outcome"] = outcomes_test
        if prediction_handler.predicted_probability_available():
            predicted_probabilities = prediction_handler.get_predicted_probabilities()
            attributes_test["PredictedProbability"] = predicted_probabilities
        if prediction_handler.predicted_outcome_available():
            predicted_outcomes = prediction_handler.get_predicted_outcomes()
            attributes_test["PredictedOutcome"] = predicted_outcomes
        return attributes_test.reset_index(drop=True, inplace=True)
    except Exception:
        raise InvalidDecisionAlgorithmParameters(sys.exc_info())


class FairnessDefinitionsCalculator:

    def __init__(self, dataset_handler, prediction_handler, descriptions, outcome_handler):
        self.descriptions = descriptions
        self.outcome_handler = outcome_handler
        self.testing_set = get_testing_set(dataset_handler, prediction_handler)

    def add_discrimination_basics(self, parameters_values):
        parameters_values["descriptions"] = self.descriptions
        parameters_values["outcome_handler"] = self.outcome_handler
        if self.testing_set["PredictedProbability"]:
            parameters_values["positives_table"], parameters_values["negatives_table"] = \
                create_positives_negatives_tables(self.testing_set, self.descriptions, parameters_values["decimals"])
            parameters_values["probabilities_table"] = \
                create_probabilities_table(parameters_values["positives_table"], parameters_values["negatives_table"],
                                           parameters_values["decimals"])
        if self.testing_set["PredictedOutcome"]:
            parameters_values["metrics"] = calculate_basic_metrics(self.testing_set, self.descriptions)

    """
    def calculate_all(self, required_parameters_values):
        self.__add_discrimination_basics(required_parameters_values)
        print(required_parameters_values)
        results = dict()
        for definition in self.__available_definitions:
            fairness_definition = getattr(self, definition["definition_name"])
            results[definition["display_name"]] = class_method(required_parameters_values)
    """