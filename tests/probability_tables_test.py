import pandas as pd

from fairness_definitions.discrimination_basics import probability_tables_calculator, create_probabilities_range


data_set_file_name = "test - dataset2.csv"
data_set = pd.read_csv(data_set_file_name, header=0)

descriptions = [{"color": "rojo"}, {"color": "azul"}]
print(descriptions)

decimals = 1
print(create_probabilities_range(decimals))

positives_table, negatives_table = probability_tables_calculator(data_set, descriptions, decimals)
print(positives_table)
print(negatives_table)
