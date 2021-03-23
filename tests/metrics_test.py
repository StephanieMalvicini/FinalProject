import pandas as pd

from fairness_definitions.discrimination_basics import basic_metrics_calculator

data_set_file_name = "test - dataset.csv"
data_set = pd.read_csv(data_set_file_name, header=0)

descriptions = [{"color": "rojo"}, {"color": "azul"}]
print(descriptions)

metrics = basic_metrics_calculator(data_set, descriptions)
print(metrics)

