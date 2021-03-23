from fairness_definitions.discrimination_basics import create_probabilities_range


def well_calibration(probabilities_table, decimals):
    length = len(probabilities_table)-1
    probabilities_values = probabilities_table[0].keys()
    satisfies_well_calibration = create_probabilities_range(decimals)
    for s in probabilities_values:
        satisfies_well_calibration[s] = True
        for i in range(length):
            if float(s) != probabilities_table[i][s]:
                satisfies_well_calibration[s] = False
                break
    return satisfies_well_calibration
