from fairness_definitions.discrimination_basics import calculate_basic_metrics
from fairness_definitions.group_fairness import group_fairness


def conditional_statistical_parity(testing_set, legitimate_attributes_list, descriptions, maximum_acceptable_difference):
    all_satisfy = True
    result = list()
    for legitimate_attributes in legitimate_attributes_list:
        satisfies, proportions = conditional_statistical_parity_aux(testing_set, legitimate_attributes,
                                                                    descriptions, maximum_acceptable_difference)
        result.append({"satisfies": satisfies, "proportions": proportions})
        all_satisfy &= satisfies
    return all_satisfy, result


def conditional_statistical_parity_aux(testing_set, legitimate_attributes, descriptions, maximum_acceptable_difference):
    testing_subset = filter_set(testing_set, legitimate_attributes)
    metrics = calculate_basic_metrics(testing_subset, descriptions)
    return group_fairness(metrics, maximum_acceptable_difference)


def filter_set(testing_set, legitimate_attributes):
    return testing_set[testing_set.eval(legitimate_attributes)]
