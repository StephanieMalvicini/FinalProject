from fairness_definitions.implementations.discrimination_basics import create_probabilities_range


def test_fairness(probabilities_table, maximum_acceptable_difference, decimals):
    subgroups_amount = len(probabilities_table)
    probabilities_values = probabilities_table[0].keys()
    satisfies_test_fairness = create_probabilities_range(decimals)
    for s in probabilities_values:
        probabilities = list()
        for i in range(subgroups_amount):
            probabilities.append(probabilities_table[i][s])
        probabilities.sort()
        if probabilities[subgroups_amount-1]-probabilities[0] > maximum_acceptable_difference:
            satisfies_test_fairness[s] = False
        else:
            satisfies_test_fairness[s] = True
    return satisfies_test_fairness
