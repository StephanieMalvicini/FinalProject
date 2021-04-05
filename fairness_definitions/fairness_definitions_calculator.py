import pandas as pd


from fairness_definitions.implementations.discrimination_basics import calculate_basic_metrics, \
    create_positives_negatives_tables

FAIRNESS_DEFINITIONS_FILENAME = "fairness_definitions/fairness_definitions.csv"
PARAMETERS_FILENAME = "fairness_definitions/fairness_definitions_parameters.csv"


class FairnessDefinitionsCalculator:

    def __init__(self, prediction_handler, dataset_handler, descriptions):
        self.prediction_handler = prediction_handler
        self.dataset_handler = dataset_handler
        self.descriptions = descriptions
        self.__available_definitions = self.__get_available_definitions()
        self.__required_parameters = self.__get_required_parameters()
        self.testing_set = self.__get_testing_set()

    def __get_available_definitions(self):
        definitions = pd.read_csv(FAIRNESS_DEFINITIONS_FILENAME)
        requirements = list()
        if not self.prediction_handler.predicted_outcome_available():
            requirements.append("predicted_outcome != 'required'")
        if not self.prediction_handler.predicted_probability_available():
            requirements.append("predicted_probability != 'required'")
        if not self.prediction_handler.distances_available():
            requirements.append("distances != 'required'")
        if not self.dataset_handler.has_outcome():
            requirements.append("outcome != 'required'")
        all_requirements = " & ".join(requirements)
        return definitions[definitions.eval(all_requirements)]

    def __get_required_parameters(self):
        parameters = pd.read_csv(PARAMETERS_FILENAME)
        required_parameters = list()
        for parameter in parameters["parameter_name"]:
            required_parameters.append("required" in self.__available_definitions[parameter].unique())
        return parameters[required_parameters]

    def __get_testing_set(self):
        attributes_test, outcomes_test = self.dataset_handler.get_testing_dataset()
        if self.dataset_handler.has_outcome:
            attributes_test["Outcome"] = outcomes_test
        if self.prediction_handler.predicted_probability_available():
            predicted_probabilities = self.prediction_handler.get_predicted_probabilities()
            attributes_test["PredictedProbability"] = predicted_probabilities
        if self.prediction_handler.predicted_outcome_available():
            predicted_outcomes = self.prediction_handler.get_predicted_outcomes()
            attributes_test["PredictedOutcome"] = predicted_outcomes
        return attributes_test.reset_index(drop=True, inplace=True)

    def __add_discrimination_basics(self, parameters_values):
        parameters_values["descriptions"] = self.descriptions
        if self.prediction_handler.predicted_probability_available():
            parameters_values["positives_table"], parameters_values["negatives_table"] = \
                create_positives_negatives_tables(self.testing_set, self.descriptions, parameters_values["decimals"])
        if self.prediction_handler.predicted_outcome_available():
            parameters_values["metrics"] = calculate_basic_metrics(self.testing_set, self.descriptions)

    def get_available_definitions_names(self):
        return self.__available_definitions["display_name"]

    def get_required_parameters_names(self):
        return self.__required_parameters["display_name"]

    """
    def calculate_all(self, required_parameters_values):
        self.__add_discrimination_basics(required_parameters_values)
        print(required_parameters_values)
        results = dict()
        for definition in self.__available_definitions:
            fairness_definition = getattr(self, definition["definition_name"])
            results[definition["display_name"]] = class_method(required_parameters_values)

#        TENGO QUE SACAR EL CALCULO DE LA PROBABILITIES TABLE DEL TESTFAIRNESS PARA PODER USARLO COMO PARAMETRO
    """