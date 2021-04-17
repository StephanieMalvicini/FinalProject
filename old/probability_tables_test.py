import pandas as pd

from fairness_definitions.discrimination_basics import \
    create_probabilities_range, create_positives_negatives_tables, create_probabilities_table

from fairness_definitions.well_calibration import well_calibration
from fairness_definitions.test_fairness import test_fairness

data_set_file_name = "test - dataset2.csv"
data_set = pd.read_csv(data_set_file_name, header=0)

descriptions = [{"color": "rojo"}, {"color": "azul"}]
print(descriptions)

decimals = 1
print(create_probabilities_range(decimals))

positives_table, negatives_table = create_positives_negatives_tables(data_set, descriptions, decimals)
print("Tabla positivos: ", positives_table)
print("Tabla negativos: ", negatives_table)

probability_table = create_probabilities_table(positives_table, negatives_table, decimals)
print("Tabla probabilidades: ")
for prob in probability_table:
    print("     ", prob)

well_calibration = well_calibration(probability_table, decimals)
print(well_calibration)

test_fairness = test_fairness(probability_table, 0.5, decimals)
print(test_fairness)
