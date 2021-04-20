from fairness_definitions.false_negative_error_rate_balance import false_negative_error_rate_balance
from fairness_definitions.false_positive_error_rate_balance import false_positive_error_rate_balance


def equalized_odds(metrics, maximum_acceptable_difference):
    satisfies_false_negative_error_rate_balance, fnr = \
        false_negative_error_rate_balance(metrics, maximum_acceptable_difference)
    satisfies_false_positive_error_rate_balance, fpr = \
        false_positive_error_rate_balance(metrics, maximum_acceptable_difference)
    return satisfies_false_positive_error_rate_balance & satisfies_false_negative_error_rate_balance, fnr, fpr
