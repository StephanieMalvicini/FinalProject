from fairness_definitions.balance_for_negative_class import balance_for_negative_class
from fairness_definitions.balance_for_positive_class import balance_for_positive_class
from fairness_definitions.causal_discrimination import causal_discrimination
from fairness_definitions.conditional_statistical_parity import conditional_statistical_parity
from fairness_definitions.conditional_use_accuracy_equality import conditional_use_accuracy_equality
from fairness_definitions.equalized_odds import equalized_odds
from fairness_definitions.fairness_through_awareness import fairness_through_awareness
from fairness_definitions.false_negative_error_rate_balance import false_negative_error_rate_balance
from fairness_definitions.false_positive_error_rate_balance import false_positive_error_rate_balance
from fairness_definitions.group_fairness import group_fairness
from fairness_definitions.overall_accuracy_equality import overall_accuracy_equality
from fairness_definitions.predictive_parity import predictive_parity
from fairness_definitions.test_fairness import test_fairness
from fairness_definitions.treatment_equality import treatment_equality
from fairness_definitions.well_calibration import well_calibration
from handlers.definitions_results import *

MAXIMUM_FAILING_PERCENTAGE = 0.1
PREDICTED_OUTCOME = "SalidaPredicha"
PREDICTED_PROBABILITY = "ProbabilidadPredicha"


def causal_discrimination_aux(parameters):
    percentage, testing_suite = causal_discrimination(parameters["testing_set"],
                                                      parameters["descriptions"],
                                                      parameters["confidence"],
                                                      parameters["error"],
                                                      parameters["minimum_samples_amount"],
                                                      parameters["prediction_handler"])
    result = Result(percentage >= MAXIMUM_FAILING_PERCENTAGE)
    result.add_element(SingleElement("confidence", parameters["confidence"]))
    result.add_element(SingleElement("error", parameters["error"]))
    result.add_element(SingleElement("minimum_samples_amount", parameters["minimum_samples_amount"]))
    result.add_element(SingleElement("Porcentaje que no satisface", percentage*100))
    # arrange attributes so the ones used in the descriptions goes first
    sorted_columns = list(parameters["descriptions"][0].keys())
    sorted_columns.insert(0, "PredictedOutcome")
    for column in testing_suite.columns:
        if column not in sorted_columns:
            sorted_columns.append(column)
    testing_suite = testing_suite[sorted_columns]
    testing_suite.rename(columns={"PredictedOutcome": PREDICTED_OUTCOME})
    column_names = list(testing_suite.columns)
    data = testing_suite.values.tolist()
    result.add_element(TableElement("Conjunto de pruebas", column_names, data))
    return result


def format_descriptions(descriptions):
    formatted_descriptions = ["{}={}".format(name, value) for name, value in descriptions.items()]
    formatted_descriptions = ",".join(formatted_descriptions)
    return formatted_descriptions


def conditional_statistical_parity_aux(parameters):
    all_satisfy = True
    results = list()
    for legitimate_attributes in parameters["legitimate_attributes_list"]:
        satisfies, proportions = conditional_statistical_parity(parameters["testing_set"],
                                                                legitimate_attributes,
                                                                parameters["descriptions"],
                                                                parameters["maximum_acceptable_difference"],
                                                                parameters["outcome_handler"])
        list_name = legitimate_attributes.split(" & ")
        list_name = [item[1:-1] for item in list_name]
        list_name = ",".join(list_name)
        list_name = "l: {}".format(list_name)
        proportions_names = list()
        for description in parameters["descriptions"]:
            proportions_names.append("P({}=1|L=l,{})".format(PREDICTED_OUTCOME,
                                                             format_descriptions(description)))
        single_result = Result(satisfies)
        single_result.add_element(ListElement(list_name, proportions_names, proportions))  # (tp+fp)/(tp+fp+tn+fn)
        results.append(single_result)
        all_satisfy &= satisfies
    final_result = Result(all_satisfy)
    final_result.add_element(
        SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    for result in results:
        final_result.add_element(result)
    return final_result


def conditional_use_accuracy_equality_aux(parameters):
    satisfies, ppv, npv = conditional_use_accuracy_equality(parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    ppv_names = list()
    npv_names = list()
    for description in parameters["descriptions"]:
        formatted_description = format_descriptions(description)
        ppv_names.append("P({}={}|{}={},{})".format(parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    formatted_description))
        npv_names.append("P({}={}|{}={},{})".format(parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    formatted_description))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("PPV", ppv_names, ppv))
    result.add_element(ListElement("NPV", npv_names, npv))
    return result


def equalized_odds_aux(parameters):
    satisfies, fnr, fpr = equalized_odds(parameters["metrics"],
                                         parameters["maximum_acceptable_difference"])
    fnr_names = list()
    fpr_names = list()
    for description in parameters["descriptions"]:
        formatted_description = format_descriptions(description)
        fnr_names.append("P({}={}|{}={},{})".format(PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    formatted_description))
        fpr_names.append("P({}={}|{}={},{})".format(PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    formatted_description))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("FNR", fnr_names, fnr))
    result.add_element(ListElement("FPR", fpr_names, fpr))
    return result


def fairness_through_awareness_aux(parameters):
    percentage, failing_cases = fairness_through_awareness(parameters["testing_set"],
                                                           parameters["decision_algorithm"],
                                                           parameters["confidence"],
                                                           parameters["error"],
                                                           parameters["minimum_samples_amount"])
    result = Result(percentage <= MAXIMUM_FAILING_PERCENTAGE)
    result.add_element(SingleElement("Porcentaje que no satisface", percentage*100))
    """for case in failing_cases:
        result.add_element(SingleElement("Sujeto 1", format_descriptions(case.individual1.to_dict())))
        result.add_element(SingleElement("Sujeto 2", format_descriptions(case.individual2.to_dict())))
        result.add_element(SingleElement("Distancia entre sujetos", case.individuals_distance))
        result.add_element(SingleElement("Distancia entre salidas", case.outcomes_distance))
    """
    return result


def balance_for_negative_class_aux(parameters):
    satisfies, expected_values = balance_for_negative_class(parameters["negatives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    expected_values_names = list()
    for description in parameters["descriptions"]:
        expected_values_names.append("E({}|{}={},{})".format(PREDICTED_PROBABILITY,
                                                             parameters["outcome_handler"].outcome_name,
                                                             parameters["outcome_handler"].negative_outcome,
                                                             format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("Esperanza", expected_values_names, expected_values))
    return result


def balance_for_positive_class_aux(parameters):
    satisfies, expected_values = balance_for_positive_class(parameters["positives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    expected_values_names = list()
    for description in parameters["descriptions"]:
        expected_values_names.append("E({}|{}={},{})".format(PREDICTED_PROBABILITY,
                                                             parameters["outcome_handler"].outcome_name,
                                                             parameters["outcome_handler"].positive_outcome,
                                                             format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("Esperanza", expected_values_names, expected_values))
    return result


def false_negative_error_rate_balance_aux(parameters):
    satisfies, fnr = false_negative_error_rate_balance(parameters["metrics"],
                                                       parameters["maximum_acceptable_difference"])
    fnr_names = list()
    for description in parameters["descriptions"]:
        fnr_names.append("P({}={}|{}={},{})".format(PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("FNR", fnr_names, fnr))
    return result


def false_positive_error_rate_balance_aux(parameters):
    satisfies, fpr = false_positive_error_rate_balance(parameters["metrics"],
                                                       parameters["maximum_acceptable_difference"])
    fpr_names = list()
    for description in parameters["descriptions"]:
        fpr_names.append("P({}={}|{}={},{})".format(PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].negative_outcome,
                                                    format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("FPR", fpr_names, fpr))
    return result


def group_fairness_aux(parameters):
    satisfies, proportions = group_fairness(parameters["metrics"],
                                            parameters["maximum_acceptable_difference"])
    proportions_names = list()
    for description in parameters["descriptions"]:
        proportions_names.append("P({}={}|{})".format(PREDICTED_OUTCOME,
                                                      parameters["outcome_handler"].positive_outcome,
                                                      format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("Proporciones", proportions_names, proportions))  # (tp+fp)/(tp+fp+tn+fn)
    return result


def overall_accuracy_equality_aux(parameters):
    satisfies, precisions = overall_accuracy_equality(parameters["metrics"],
                                                      parameters["maximum_acceptable_difference"])
    precisions_names = list()
    for description in parameters["descriptions"]:
        precisions_names.append("P({}={}|{})".format(PREDICTED_OUTCOME,
                                                     parameters["outcome_handler"].outcome_name,
                                                     format_descriptions(description)))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("Precisiones", precisions_names, precisions))  # (tp+tn)/(tp+fp+tn+fn)
    return result


def predictive_parity_aux(parameters):
    satisfies, ppv = predictive_parity(parameters["metrics"],
                                       parameters["maximum_acceptable_difference"])
    ppv_names = list()
    for description in parameters["descriptions"]:
        formatted_description = format_descriptions(description)
        ppv_names.append("P({}={}|{}={},{})".format(parameters["outcome_handler"].outcome_name,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    PREDICTED_OUTCOME,
                                                    parameters["outcome_handler"].positive_outcome,
                                                    formatted_description))
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("PPV", ppv_names, ppv))
    return result


def treatment_equality_aux(parameters):
    satisfies, errors = treatment_equality(parameters["metrics"],
                                           parameters["maximum_acceptable_difference"])
    errors_names = [format_descriptions(description) for description in parameters["descriptions"]]
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(ListElement("Errores", errors_names, errors))  # fn/fp
    return result


def add_probabilities_table_parameter(result, parameters):
    row_descriptions = list()
    template = "P({}={}|S=s,{})"
    for description in parameters["descriptions"]:
        formatted_description = format_descriptions(description)
        row_descriptions.append(template.format(parameters["outcome_handler"].outcome_name,
                                                parameters["outcome_handler"].positive_outcome,
                                                formatted_description))
    column_names = list(parameters["probabilities_table"][0].keys())
    column_names.insert(0, "s")
    data = [list(dict_probabilities.values()) for dict_probabilities in parameters["probabilities_table"]]
    for i, row in enumerate(data):
        row.insert(0, row_descriptions[i])
    result.add_element(TableElement("probabilities_table", column_names, data))


def test_fairness_aux(parameters):
    satisfies = test_fairness(parameters["probabilities_table"],
                              parameters["maximum_acceptable_difference"],
                              parameters["decimals"])
    result = Result(satisfies)
    result.add_element(SingleElement("maximum_acceptable_difference", parameters["maximum_acceptable_difference"]))
    result.add_element(SingleElement("decimals", parameters["decimals"]))
    add_probabilities_table_parameter(result, parameters)
    return result


def well_calibration_aux(parameters):
    satisfies = well_calibration(parameters["probabilities_table"],
                                 parameters["decimals"])
    result = Result(satisfies)
    result.add_element(SingleElement("decimals", parameters["decimals"]))
    add_probabilities_table_parameter(result, parameters)
    return result
