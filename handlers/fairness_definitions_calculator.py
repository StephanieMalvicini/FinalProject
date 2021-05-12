import sys

from databases import parameters
from exceptions.decision_algorithm import InvalidDecisionAlgorithmParameters
from fairness_definitions.discrimination_basics import calculate_basic_metrics, \
    create_positives_negatives_tables, create_probabilities_table
from handlers import fairness_definitions_adapter
from handlers.parameters_results import ParametersResult


class FairnessDefinitionsCalculator:

    def __init__(self, dataset_handler, prediction_handler, positive_outcome, negative_outcome, outcome_name):
        self.dataset_handler = dataset_handler
        self.prediction_handler = prediction_handler
        self.testing_set = self.get_testing_set()
        self.params = self.create_parameters(positive_outcome, negative_outcome, outcome_name)

    def get_testing_set(self):
        try:
            attributes_test, outcomes_test = self.dataset_handler.get_testing_dataset()
            if self.dataset_handler.has_outcome():
                attributes_test["Outcome"] = outcomes_test
            if self.prediction_handler.predicted_probability_available():
                predicted_probabilities = self.prediction_handler.get_predicted_probabilities()
                attributes_test["PredictedProbability"] = predicted_probabilities
            if self.prediction_handler.predicted_outcome_available():
                predicted_outcomes = self.prediction_handler.get_predicted_outcomes()
                attributes_test["PredictedOutcome"] = predicted_outcomes
        except Exception:
            raise InvalidDecisionAlgorithmParameters(sys.exc_info())
        return attributes_test

    def calculate(self, fairness_definitions):
        results = dict()
        parameters_result = ParametersResult(parameters.get_all())
        for definition_name in fairness_definitions:
            fairness_definition_method = getattr(fairness_definitions_adapter, "{}_aux".format(definition_name))
            results[definition_name] = fairness_definition_method(self.params, parameters_result)
        return results

    def create_parameters(self, positive_outcome, negative_outcome, outcome_name):
        params = dict()
        params["testing_set"] = self.testing_set
        params["positive_outcome"] = positive_outcome
        params["negative_outcome"] = negative_outcome
        params["prediction_handler"] = self.prediction_handler
        params["outcome_name"] = outcome_name
        params["decision_algorithm"] = self.prediction_handler.decision_algorithm #SACARLO!!
        return params

    def update_parameters(self, descriptions, new_params):
        old_descriptions = self.params["descriptions"] if "descriptions" in self.params.keys() else None
        old_decimals = self.params["decimals"] if "decimals" in self.params.keys() else None
        self.params["descriptions"] = descriptions
        for (name, value) in new_params.items():
            self.params[name] = value
        if old_descriptions != self.params["descriptions"]:
            self.update_metrics()
            if "decimals" in self.params.keys():
                self.update_tables()
        elif "decimals" in self.params.keys() and old_decimals != self.params["decimals"]:
            self.update_tables()

    def update_tables(self):
        if self.prediction_handler.predicted_probability_available():
            self.params["positives_table"], self.params["negatives_table"] = \
                create_positives_negatives_tables(self.testing_set,
                                                  self.params["descriptions"],
                                                  self.params["decimals"],
                                                  self.params["positive_outcome"])
            self.params["probabilities_table"] = create_probabilities_table(
                self.params["positives_table"], self.params["negatives_table"], self.params["decimals"])

    def update_metrics(self):
        if self.prediction_handler.predicted_outcome_available() and self.dataset_handler.has_outcome():
            self.params["metrics"] = calculate_basic_metrics(self.testing_set,
                                                             self.params["descriptions"],
                                                             self.params["positive_outcome"],
                                                             self.params["negative_outcome"])

    def get_basic_metrics(self):
        if "metrics" in self.params.keys():
            return self.params["metrics"]
        return None

    def get_positives_negatives_table(self):
        if "positives_table" in self.params.keys():
            return self.params["positives_table"], self.params["negatives_table"]
        return None, None
