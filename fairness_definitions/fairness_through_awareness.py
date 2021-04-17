import copy
import math


def fairness_through_awareness(testing_set, decision_algorithm):
    not_satisfies = 0
    individuals_amount = len(testing_set)
    for i in range(individuals_amount-1):
        for first in range(i+1, individuals_amount):
            individual1 = clone_and_remove_added_attributes(testing_set.iloc[i])
            individual2 = clone_and_remove_added_attributes(testing_set.iloc[first])
            individuals_distance = decision_algorithm.individuals_distance(individual1, individual2)
            outcomes_distance = decision_algorithm.outcomes_distance(individual1["PredictedOutcome"],
                                                                     individual2["PredictedOutcome"])
            if outcomes_distance > individuals_distance:
                not_satisfies += 1
    total_combinations = math.factorial(individuals_amount)/(2*math.factorial(individuals_amount-2))
    not_satisfies_percentage = not_satisfies/total_combinations * 100
    return not_satisfies_percentage


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
