import math

from constants import statistical_constants
from constants.predictions_names import PREDICTED_OUTCOME


class FailingCase:

    def __init__(self, individual1, individual2, individuals_distance, outcomes_distance):
        self.individual1 = individual1
        self.individual2 = individual2
        self.individuals_distance = individuals_distance
        self.outcomes_distance = outcomes_distance


def fairness_through_awareness(testing_set, calculate_individuals_distance, calculate_outcomes_distance,
                               confidence, error, minimum_samples_amount):
    not_satisfies = 0
    individuals_amount = len(testing_set.index)
    failing_cases = list()
    verified_cases = 0
    confidence_reached = False
    for i in range(individuals_amount-1):
        individual1 = testing_set.iloc[i]
        for first in range(i+1, individuals_amount):
            verified_cases += 1
            individual2 = testing_set.iloc[first]
            individuals_distance = calculate_individuals_distance(individual1, individual2)
            outcomes_distance = \
                calculate_outcomes_distance(individual1[PREDICTED_OUTCOME], individual2[PREDICTED_OUTCOME])
            if outcomes_distance > individuals_distance:
                not_satisfies += 1
                failing_cases.append(FailingCase(individual1, individual2, individuals_distance, outcomes_distance))
            if verified_cases > minimum_samples_amount:
                p = not_satisfies / verified_cases
                current_error = statistical_constants.CONFIDENCE_Z_VALUES[confidence] * math.sqrt(
                    p * (1 - p) / verified_cases)
                if current_error < error:
                    confidence_reached = True
                    return p, failing_cases, confidence_reached
    return not_satisfies / verified_cases, failing_cases, confidence_reached

