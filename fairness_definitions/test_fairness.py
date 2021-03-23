import copy

from fairness_definitions.discrimination_basics import create_probabilities_range


def test_fairness(positives_table, negatives_table, maximum_acceptable_difference, decimals):
    length = len(positives_table)
    probabilities_values = positives_table[0].keys()
    probabilities_table = list()
    probabilities = list()
    probabilities_range = create_probabilities_range(decimals)
    for _ in range(length+1):
        probabilities_table.append(copy.deepcopy(probabilities_range))
    for s in probabilities_values:
        for i in range(length):
            if positives_table[i][s]+negatives_table[i][s] > 0:
                probability = positives_table[i][s]/(positives_table[i][s]+negatives_table[i][s])
            else:
                probability = 0
            probabilities.append(probability)
            probabilities_table[i][s] = probability
        probabilities.sort()
        if probabilities[length-1]-probabilities[0] > maximum_acceptable_difference:
            probabilities_table[length][s] = False
        else:
            probabilities_table[length][s] = True
    return probabilities_table
