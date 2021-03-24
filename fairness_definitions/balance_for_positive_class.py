def balance_for_positive_class(positives_table, metrics, maximum_acceptable_difference):
    satisfies_balance_for_positive_class = True
    groups_amount = len(positives_table)
    probabilities_values = positives_table[0].keys()
    expected_values = [0] * groups_amount
    for i in range(groups_amount):
        for s in probabilities_values:
            if metrics[i]["TP"]+metrics[i]["FN"] > 0:
                expected_values[i] += (s * positives_table[i][s]/(metrics[i]["TP"]+metrics[i]["FN"]))
    sorted_expected_values = sorted(expected_values)
    if sorted_expected_values[groups_amount - 1] - sorted_expected_values[0] > maximum_acceptable_difference:
        satisfies_balance_for_positive_class = False
    return satisfies_balance_for_positive_class, expected_values
