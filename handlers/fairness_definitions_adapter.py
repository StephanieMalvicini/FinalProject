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
from handlers.results import Result

MAXIMUM_FAILING_PROPORTION = 0.1


def causal_discrimination_aux(parameters, parameters_result):
    proportion, test_suite, confidence_reached = causal_discrimination(parameters["testing_set"],
                                                                       parameters["descriptions"],
                                                                       parameters["confidence"],
                                                                       parameters["error"] / 100,
                                                                       parameters["minimum_samples_amount"],
                                                                       parameters["prediction_handler"])
    result = Result(proportion <= MAXIMUM_FAILING_PROPORTION)
    parameters_result.add_confidence(result, parameters["confidence"], confidence_reached)
    parameters_result.add_percentage(result, proportion, parameters["error"])
    parameters_result.add_minimum_samples_amount(result, parameters["minimum_samples_amount"])
    parameters_result.add_test_suite(result, test_suite, parameters["descriptions"])
    return result


def conditional_statistical_parity_aux(parameters, parameters_result):
    all_satisfy = True
    results = list()
    for legitimate_attributes in parameters["legitimate_attributes_list"]:
        satisfies, proportions = conditional_statistical_parity(parameters["testing_set"],
                                                                legitimate_attributes,
                                                                parameters["descriptions"],
                                                                parameters["maximum_acceptable_difference"],
                                                                parameters["positive_outcome"],
                                                                parameters["negative_outcome"])
        template = "P({}=1|L,{})".format(parameters_result.predicted_outcome_display_name(), "{}")
        single_result = Result(satisfies)
        parameters_result.add_legitimate_attributes(single_result, legitimate_attributes, proportions, template,
                                                    parameters["descriptions"])
        results.append(single_result)
        all_satisfy &= satisfies
    final_result = Result(all_satisfy)
    parameters_result.add_maximum_acceptable_difference(final_result, parameters["maximum_acceptable_difference"])
    for result in results:
        final_result.add_element(result)
    return final_result


def conditional_use_accuracy_equality_aux(parameters, parameters_result):
    satisfies, ppv_values, npv_values = conditional_use_accuracy_equality(parameters["metrics"],
                                                                          parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])

    template = "P({}={}|{}={},{})".format(parameters["outcome_name"],
                                          "{}",
                                          parameters_result.predicted_outcome_display_name(),
                                          "{}", "{}")
    ppv_template = template.format(parameters["positive_outcome"],
                                   parameters["positive_outcome"], "{}")
    npv_template = template.format(parameters["negative_outcome"],
                                   parameters["negative_outcome"], "{}")
    parameters_result.add_list(result, "PPV", ppv_values, ppv_template, parameters["descriptions"])
    parameters_result.add_list(result, "FPR", npv_values, npv_template, parameters["descriptions"])
    return result


def equalized_odds_aux(parameters, parameters_result):
    satisfies, tpr_values, fpr_values = equalized_odds(parameters["metrics"],
                                                       parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{}={},{})".format(parameters_result.predicted_outcome_display_name(),
                                          parameters["positive_outcome"],
                                          parameters["outcome_name"],
                                          "{}", "{}")
    tpr_template = template.format(parameters["positive_outcome"], "{}")
    fpr_template = template.format(parameters["negative_outcome"], "{}")
    parameters_result.add_list(result, "TPR", tpr_values, tpr_template, parameters["descriptions"])
    parameters_result.add_list(result, "FPR", fpr_values, fpr_template, parameters["descriptions"])
    return result


def fairness_through_awareness_aux(parameters, parameters_result):
    proportion, failing_cases, confidence_reached = fairness_through_awareness(parameters["testing_set"],
                                                                               parameters["decision_algorithm"],
                                                                               parameters["confidence"],
                                                                               parameters["error"] / 100,
                                                                               parameters["minimum_samples_amount"])
    result = Result(proportion <= MAXIMUM_FAILING_PROPORTION)
    parameters_result.add_confidence(result, parameters["confidence"], confidence_reached)
    parameters_result.add_percentage(result, proportion, parameters["error"])
    parameters_result.add_minimum_samples_amount(result, parameters["minimum_samples_amount"])
    parameters_result.add_failing_cases(result, failing_cases)
    return result


def balance_for_negative_class_aux(parameters, parameters_result):
    satisfies, expected_values = balance_for_negative_class(parameters["negatives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "E({}|{}={},{})".format(parameters_result.predicted_probability_display_name(),
                                       parameters["outcome_name"],
                                       parameters["negative_outcome"],
                                       "{}")
    parameters_result.add_list(result, "expected_values", expected_values, template, parameters["descriptions"])
    return result


def balance_for_positive_class_aux(parameters, parameters_result):
    satisfies, expected_values = balance_for_positive_class(parameters["positives_table"],
                                                            parameters["metrics"],
                                                            parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "E({}|{}={},{})".format(parameters_result.predicted_probability_display_name(),
                                       parameters["outcome_name"],
                                       parameters["positive_outcome"],
                                       "{}")
    parameters_result.add_list(result, "expected_values", expected_values, template, parameters["descriptions"])
    return result


def false_negative_error_rate_balance_aux(parameters, parameters_result):
    satisfies, fnr_values = false_negative_error_rate_balance(parameters["metrics"],
                                                              parameters["maximum_acceptable_difference"])

    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{}={},{})".format(parameters_result.predicted_outcome_display_name(),
                                          parameters["negative_outcome"],
                                          parameters["outcome_name"],
                                          parameters["positive_outcome"],
                                          "{}")
    parameters_result.add_list(result, "FNR", fnr_values, template, parameters["descriptions"])
    return result


def false_positive_error_rate_balance_aux(parameters, parameters_result):
    satisfies, fpr_values = false_positive_error_rate_balance(parameters["metrics"],
                                                              parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{}={},{})".format(parameters_result.predicted_outcome_display_name(),
                                          parameters["positive_outcome"],
                                          parameters["outcome_name"],
                                          parameters["negative_outcome"],
                                          "{}")
    parameters_result.add_list(result, "FPR", fpr_values, template, parameters["descriptions"])
    return result


def group_fairness_aux(parameters, parameters_result):
    satisfies, proportions = group_fairness(parameters["metrics"],
                                            parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{})".format(parameters_result.predicted_outcome_display_name(),
                                    parameters["positive_outcome"],
                                    "{}")
    parameters_result.add_list(result, "(TP+FP)/(TP+FP+TN+FN)", proportions, template, parameters["descriptions"])
    return result


def overall_accuracy_equality_aux(parameters, parameters_result):
    satisfies, precisions = overall_accuracy_equality(parameters["metrics"],
                                                      parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{})".format(parameters_result.predicted_outcome_display_name(),
                                    parameters["outcome_name"],
                                    "{}")
    parameters_result.add_list(result, "(TP+TN)/(TP+FP+TN+FN)", precisions, template, parameters["descriptions"])
    return result


def predictive_parity_aux(parameters, parameters_result):
    satisfies, ppv_values = predictive_parity(parameters["metrics"],
                                              parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    template = "P({}={}|{}={},{})".format(parameters["outcome_name"],
                                          parameters["positive_outcome"],
                                          parameters_result.predicted_outcome_display_name(),
                                          parameters["positive_outcome"],
                                          "{}")
    parameters_result.add_list(result, "PPV", ppv_values, template, parameters["descriptions"])
    return result


def treatment_equality_aux(parameters, parameters_result):
    satisfies, errors = treatment_equality(parameters["metrics"],
                                           parameters["maximum_acceptable_difference"])
    result = Result(satisfies)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    parameters_result.add_list(result, "FN/FP", errors, "[{}]", parameters["descriptions"])
    return result


def test_fairness_aux(parameters, parameters_result):
    satisfies_list = test_fairness(parameters["probabilities_table"],
                                   parameters["maximum_acceptable_difference"],
                                   parameters["decimals"])
    result = Result(True in satisfies_list)
    parameters_result.add_maximum_acceptable_difference(result, parameters["maximum_acceptable_difference"])
    parameters_result.add_decimals(result, parameters["decimals"])
    template = "P({}={}|S=s,{})".format(parameters["outcome_name"],
                                        parameters["positive_outcome"],
                                        "{}")
    parameters_result.add_probabilities_table(result, template, satisfies_list, parameters["descriptions"],
                                              parameters["probabilities_table"])
    return result


def well_calibration_aux(parameters, parameters_result):
    satisfies_list = well_calibration(parameters["probabilities_table"],
                                      parameters["decimals"])
    result = Result(True in satisfies_list)
    parameters_result.add_decimals(result, parameters["decimals"])
    template = "P({}={}|S=s,{})".format(parameters["outcome_name"],
                                        parameters["positive_outcome"],
                                        "{}")
    parameters_result.add_probabilities_table(result, template, satisfies_list, parameters["descriptions"],
                                              parameters["probabilities_table"])
    return result
