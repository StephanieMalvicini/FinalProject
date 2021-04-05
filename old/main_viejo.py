import copy

import pandas as pd
from sklearn.model_selection import train_test_split

from fairness_definitions.implementations.causal_discrimination import causal_discrimination
from fairness_definitions.implementations.discrimination_basics import calculate_basic_metrics, calculate_probability_tables
from fairness_definitions.implementations.group_fairness import group_fairness
from fairness_definitions.implementations.conditional_statistical_parity import conditional_statistical_parity
from fairness_definitions.implementations.predictive_parity import predictive_parity
from fairness_definitions.implementations.test_fairness import test_fairness
from fairness_definitions.implementations.well_calibration import well_calibration

from decision_algorithms.creator import Creator

pd.set_option('mode.chained_assignment', None)

data_set_file_name = "../datasets/germandata-gender.csv"
# data_set = pd.read_csv(data_set_file_name, header=0)

# borrarle el index a los csv que vaya a usar
#index = "Unnamed: 0"
#data_set = data_set.set_index(index)

#column_names = data_set.columns

# Agregar otro metodo al algoritmo de decision para que formatee el dataset si corresponde
for (column, type) in data_set.dtypes.items():
    if type == "object":
        data_set[column] = data_set[column].astype('category')
        data_set[column] = data_set[column].cat.codes
# Agregar una clase que se encarge de obetener attributes_train, attributes_test, outcomes_train, outcomes_test (y tenga un add column)

# print(data_set.dtypes)

# se las muestro al usuario y elige el outcome
outcome = "credit_score"
column_names = column_names.drop(outcome)

# print(column_names)
attributes = data_set[column_names]
outcomes = data_set[outcome]
attributes_train, attributes_test, outcomes_train, outcomes_test = \
    train_test_split(attributes, outcomes, test_size=0.10, random_state=0)

# decision_algorithm = Creator().factory_method("logistic_regression_classifier", attributes_train, outcomes_train)
decision_algorithm = Creator().factory_method("logistic_regression_classifier", attributes_train, outcomes_train)

testing_set = copy.deepcopy(attributes_test)  # para el causal, los otros necesitan el attributes_test

predicted_outcomes = decision_algorithm.predict_outcome(attributes_test)
predicted_probabilities = decision_algorithm.predict_probability(attributes_test)
attributes_test["Outcome"] = outcomes_test
attributes_test["PredictedOutcome"] = predicted_outcomes
testing_set["PredictedOutcome"] = predicted_outcomes
attributes_test["PredictedProbability"] = predicted_probabilities[:, 1]
attributes_test.reset_index(drop=True, inplace=True)
testing_set.reset_index(drop=True, inplace=True)
# print(attributes_test.to_string())
# print(attributes_test.iloc[249].to_dict())

descriptions = [{"present_residence_since": 1}, {"present_residence_since": 2}, {"present_residence_since": 3}, {"present_residence_since": 4}]
# descriptions = [{"personal_status_and_gender": 0.0}, {"personal_status_and_gender": 1.0}]
# print(testing_set.to_string())

causal_discrimination = causal_discrimination(testing_set, descriptions, 0.99, 0.1, len(testing_set.index),
                                              decision_algorithm)
# causal_discrimination = causal_discrimination(testing_set, descriptions, 0.99, 0.1, 1, decision_algorithm)
print("causal discrimination: ", causal_discrimination)

metrics = calculate_basic_metrics(attributes_test, descriptions)
maximum_acceptable_difference = 0.05

group_fairness, proportions = group_fairness(metrics, maximum_acceptable_difference)
print("group fairness: ", group_fairness)
print("proportions: ", proportions)

legitimate_attributes_list = ["credit_amount>=10000 & (job == 3)", "savings > 0", "personal_status_and_gender == 0"]
# legitimate_attributes = "credit_amount>=10000 & (job == 3)"
# mostrar todas las columnas y que el usuario las elija,
# si es numero que muestre >, >=, <, <=, ==. Si mo es numero que muestre solo == y quizas las opciones posibles
# puede repetir la tarea multiples veces, generando mas de una descripcion o grupo. por eso hay un arreglo de strings, y no un string solo
conditional_statistical_parity, proportions = conditional_statistical_parity(attributes_test, legitimate_attributes_list, descriptions, maximum_acceptable_difference)
print("conditional statistical parity: ", conditional_statistical_parity)
print("proportions: ", proportions)

predictive_parity, ppv = predictive_parity(metrics, maximum_acceptable_difference)
print("predictive parity: ", predictive_parity)
print("ppv: ", ppv)

decimals = 1
positives_table, negatives_table = calculate_probability_tables(attributes_test, descriptions, decimals)
test_fairness = test_fairness(positives_table, negatives_table, maximum_acceptable_difference, decimals)
print("test fairness: ", test_fairness)

well_calibration = well_calibration(test_fairness, decimals)
print("well calibration: ", well_calibration)
