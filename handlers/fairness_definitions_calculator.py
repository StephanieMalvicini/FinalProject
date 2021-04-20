from fairness_definitions.discrimination_basics import calculate_basic_metrics, \
    create_positives_negatives_tables, create_probabilities_table
from handlers import fairness_definitions


def get_testing_set(dataset_handler, prediction_handler):
    #try:
    attributes_test, outcomes_test = dataset_handler.get_testing_dataset()
    if dataset_handler.has_outcome():
        attributes_test["Outcome"] = outcomes_test
    if prediction_handler.predicted_probability_available():
        predicted_probabilities = prediction_handler.get_predicted_probabilities()
        attributes_test["PredictedProbability"] = predicted_probabilities
    if prediction_handler.predicted_outcome_available():
        predicted_outcomes = prediction_handler.get_predicted_outcomes()
        attributes_test["PredictedOutcome"] = predicted_outcomes
    attributes_test.reset_index(drop=True, inplace=True)
    return attributes_test
    #except Exception:
    #    raise InvalidDecisionAlgorithmParameters(sys.exc_info())


def calculate(definitions, descriptions, parameters, dataset_handler, prediction_handler, outcome_handler):
    testing_set = get_testing_set(dataset_handler, prediction_handler)
    add_parameters(testing_set, descriptions, parameters, dataset_handler, prediction_handler, outcome_handler)
    results = dict()
    for definition_name in definitions:
        fairness_definition_method = getattr(fairness_definitions, "{}_aux".format(definition_name))
        results[definition_name] = fairness_definition_method(parameters)
    return results


def add_parameters(testing_set, descriptions, parameters, dataset_handler, prediction_handler, outcome_handler):
    parameters["testing_set"] = testing_set
    parameters["descriptions"] = descriptions
    parameters["outcome_handler"] = outcome_handler
    parameters["prediction_handler"] = prediction_handler
    parameters["decision_algorithm"] = prediction_handler.decision_algorithm
    if prediction_handler.predicted_probability_available():
        parameters["positives_table"], parameters["negatives_table"] = \
            create_positives_negatives_tables(testing_set, descriptions, parameters["decimals"])
        parameters["probabilities_table"] = \
            create_probabilities_table(parameters["positives_table"], parameters["negatives_table"],
                                       parameters["decimals"])
    if prediction_handler.predicted_outcome_available() and dataset_handler.has_outcome():
        parameters["metrics"] = calculate_basic_metrics(testing_set, descriptions, outcome_handler)
