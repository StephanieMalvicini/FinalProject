from fairness_definitions.discrimination_basics import calculate_basic_metrics
from fairness_definitions.group_fairness import group_fairness


def conditional_statistical_parity(testing_set, legitimate_attributes, descriptions, maximum_acceptable_difference,
                                   positive_outcome, negative_outcome):
    testing_subset = filter_set(testing_set, legitimate_attributes)
    metrics = calculate_basic_metrics(testing_subset, descriptions, positive_outcome, negative_outcome)
    return group_fairness(metrics, maximum_acceptable_difference)


def filter_set(testing_set, legitimate_attributes):
    return testing_set[testing_set.eval(legitimate_attributes)]
