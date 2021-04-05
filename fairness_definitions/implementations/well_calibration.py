from fairness_definitions.implementations.discrimination_basics import create_probabilities_range


def well_calibration(probabilities_table, decimals):
    subgroups_amount = len(probabilities_table)
    probabilities_values = probabilities_table[0].keys()
    satisfies_well_calibration = create_probabilities_range(decimals)
    for s in probabilities_values:
        satisfies_well_calibration[s] = True
        for i in range(subgroups_amount):
            if float(s) != probabilities_table[i][s]:
                satisfies_well_calibration[s] = False
                break
    return satisfies_well_calibration
