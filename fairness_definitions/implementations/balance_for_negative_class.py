def balance_for_negative_class(negatives_table, metrics, maximum_acceptable_difference):
    satisfies_balance_for_negative_class = True
    groups_amount = len(negatives_table)
    probabilities_values = negatives_table[0].keys()
    expected_values = [0] * groups_amount
    for i in range(groups_amount):
        for s in probabilities_values:
            if metrics[i]["TN"]+metrics[i]["FP"] > 0:
                expected_values[i] += (s * negatives_table[i][s]/(metrics[i]["TN"]+metrics[i]["FP"]))
    sorted_expected_values = sorted(expected_values)
    if sorted_expected_values[groups_amount - 1] - sorted_expected_values[0] > maximum_acceptable_difference:
        satisfies_balance_for_negative_class = False
    return satisfies_balance_for_negative_class, expected_values
