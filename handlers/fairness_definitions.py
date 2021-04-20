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


def balance_for_negative_class_aux(parameters):
    satisfies, expected_values = balance_for_negative_class(parameters["negatives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "Esperanza", expected_values)


def balance_for_positive_class_aux(parameters):
    satisfies, expected_values = balance_for_positive_class(parameters["positives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "Esperanza", expected_values)


def causal_discrimination_aux(parameters):
    percentage, testing_suite = causal_discrimination(parameters["testing_set"],
                                                      parameters["descriptions"],
                                                      parameters["confidence"],
                                                      parameters["error"],
                                                      parameters["minimum_samples_amount"],
                                                      parameters["prediction_handler"])
    return PercentageWithDataFrameResult(percentage, "Conjunto de pruebas", testing_suite)


def conditional_statistical_parity_aux(parameters):
    all_satisfy = True
    results = list()
    for legitimate_attributes in parameters["legitimate_attributes_list"]:
        satisfies, proportions = conditional_statistical_parity(parameters["testing_set"],
                                                                legitimate_attributes,
                                                                parameters["descriptions"],
                                                                parameters["maximum_acceptable_difference"],
                                                                parameters["outcome_handler"])
        results.append(ListResult(satisfies, "Proporciones", proportions))  # (tp+fp)/(tp+fp+tn+fn)
        all_satisfy &= satisfies
    return ListOfResults(all_satisfy, results)


def conditional_use_accuracy_equality_aux(parameters):
    satisfies, ppv, npv = conditional_use_accuracy_equality(parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    return DoubleListResult(satisfies, "PPV", ppv, "NPV", npv)


def equalized_odds_aux(parameters):
    satisfies, fnr, fpr = equalized_odds(parameters["metrics"],
                                         parameters["maximum_acceptable_difference"])
    return DoubleListResult(satisfies, "FNR", fnr, "FPR", fpr)


def fairness_through_awareness_aux(parameters):
    percentage, failing_cases = fairness_through_awareness(parameters["testing_set"],
                                                           parameters["decision_algorithm"])
    return PercentageWithListResult(percentage, "Casos donde falla", failing_cases)


def false_negative_error_rate_balance_aux(parameters):
    satisfies, fnr = false_negative_error_rate_balance(parameters["metrics"],
                                                       parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "FNR", fnr)


def false_positive_error_rate_balance_aux(parameters):
    satisfies, fpr = false_positive_error_rate_balance(parameters["metrics"],
                                                       parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "FPR", fpr)


def group_fairness_aux(parameters):
    satisfies, proportions = group_fairness(parameters["metrics"],
                                            parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "Proporciones", proportions)  # (tp+fp)/(tp+fp+tn+fn)


def overall_accuracy_equality_aux(parameters):
    satisfies, precisions = overall_accuracy_equality(parameters["metrics"],
                                                      parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "Precisiones", precisions)  # (tp+tn)/(tp+fp+tn+fn)


def predictive_parity_aux(parameters):
    satisfies, ppv = predictive_parity(parameters["metrics"],
                                       parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "PPV", ppv)


def test_fairness_aux(parameters):
    satisfies = test_fairness(parameters["probabilities_table"],
                              parameters["maximum_acceptable_difference"],
                              parameters["decimals"])
    return TableResult(satisfies, "Probabilidades", parameters["probabilities_table"])


def treatment_equality_aux(parameters):
    satisfies, errors = treatment_equality(parameters["metrics"],
                                           parameters["maximum_acceptable_difference"])
    return ListResult(satisfies, "Errores", errors)  # fn/fp


def well_calibration_aux(parameters):
    satisfies = well_calibration(parameters["probabilities_table"],
                                 parameters["decimals"])
    return TableResult(satisfies, "Probabilidades", parameters["probabilities_table"])
