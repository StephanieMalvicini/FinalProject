import sys

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from fairness_definitions.discrimination_basics import calculate_basic_metrics, \
    create_positives_negatives_tables, create_probabilities_table
from handlers import fairness_definitions_adapter


class FairnessDefinitionsCalculator:

    def __init__(self, dataset_handler, prediction_handler, outcome_handler):
        self.dataset_handler = dataset_handler
        self.prediction_handler = prediction_handler
        self.outcome_handler = outcome_handler
        self.testing_set = self.get_testing_set()
        self.params = self.create_parameters()

    def get_testing_set(self):
        try:
            attributes_test, outcomes_test = self.dataset_handler.get_testing_dataset()
            if self.dataset_handler.has_outcome():
                attributes_test["Outcome"] = outcomes_test
            if self.prediction_handler.predicted_probability_available():
                predicted_probabilities = self.prediction_handler.get_predicted_probabilities()
                attributes_test["PredictedProbability"] = predicted_probabilities
            if self. prediction_handler.predicted_outcome_available():
                predicted_outcomes = self.prediction_handler.get_predicted_outcomes()
                attributes_test["PredictedOutcome"] = predicted_outcomes
            attributes_test.reset_index(drop=True, inplace=True)
        except Exception:
            raise InvalidDecisionAlgorithmParameters(sys.exc_info())
        return attributes_test

    def calculate(self, fairness_definitions):
        results = dict()
        for definition_name in fairness_definitions:
            fairness_definition_method = getattr(fairness_definitions_adapter, "{}_aux".format(definition_name))
            results[definition_name] = fairness_definition_method(self.params)
        return results

    def create_parameters(self):
        params = dict()
        params["testing_set"] = self.testing_set
        params["outcome_handler"] = self.outcome_handler
        params["prediction_handler"] = self.prediction_handler
        params["decision_algorithm"] = self.prediction_handler.decision_algorithm
        return params

    def update_parameters(self, descriptions, new_params): # ver de no actualizar si no cambio
        self.params["descriptions"] = descriptions
        for (name, value) in new_params.items():
            self.params[name] = value
        self.update_tables()
        self.update_metrics()

    def update_tables(self):
        if self.prediction_handler.predicted_probability_available() and "decimals" in self.params.keys():
            self.params["positives_table"], self.params["negatives_table"] = create_positives_negatives_tables(
                self.testing_set, self.params["descriptions"], self.params["decimals"], self.outcome_handler)
            self.params["probabilities_table"] = create_probabilities_table(
                self.params["positives_table"], self.params["negatives_table"], self.params["decimals"])

    def update_metrics(self):
        if self.prediction_handler.predicted_outcome_available() and self.dataset_handler.has_outcome():
            self.params["metrics"] = \
                calculate_basic_metrics(self.testing_set, self.params["descriptions"], self.outcome_handler)

    def get_basic_metrics(self):
        if "metrics" in self.params.keys():
            return self.params["metrics"]
        return None

    def get_positives_negatives_table(self):
        if "positives_table" in self.params.keys():
            return self.params["positives_table"], self.params["negatives_table"]
        return None, None
