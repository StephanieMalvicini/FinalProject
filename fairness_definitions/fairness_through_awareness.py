import math


def fairness_through_awareness(testing_set, decision_algorithm):
    not_satisfies = 0
    individuals_amount = len(testing_set)
    for i in range(individuals_amount-1):
        for first in range(i+1, individuals_amount):
            subjects_distance = decision_algorithm.subjects_distance(testing_set.iloc[i], testing_set.iloc[first])
            outcomes_distance = decision_algorithm.outcomes_distance(testing_set.iloc[i]["PredictedOutcome"], testing_set.iloc[first]["PredictedOutcome"])
            if outcomes_distance > subjects_distance:
                not_satisfies += 1
    total_combinations = math.factorial(individuals_amount)/(2*math.factorial(individuals_amount-2))
    not_satisfies_percentage = not_satisfies/total_combinations * 100
    return not_satisfies_percentage
