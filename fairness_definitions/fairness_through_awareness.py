import copy
import math

from constants import statistical_constants


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
        individual1 = clone_and_remove_added_attributes(testing_set.iloc[i])
        for first in range(i+1, individuals_amount):
            verified_cases += 1
            individual2 = clone_and_remove_added_attributes(testing_set.iloc[first])
            individuals_distance = calculate_individuals_distance(individual1, individual2)
            outcomes_distance = \
                calculate_outcomes_distance(individual1["PredictedOutcome"], individual2["PredictedOutcome"])
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


def clone_and_remove_added_attributes(individual):
    individual_clone = copy.deepcopy(individual)
    delete_attribute(individual_clone, "Outcome")
    delete_attribute(individual_clone, "PredictedProbability")
    return individual_clone


def delete_attribute(individual, attribute_name):
    try:
        del individual[attribute_name]
    except KeyError:
        pass
