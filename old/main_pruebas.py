from handlers.dataset_handler import DatasetHandler
from decision_algorithms.creator import Creator
from fairness_definitions.fairness_definitions_calculator import FairnessDefinitionsCalculator
from handlers.descriptions_calculator import get_descriptions
from handlers.prediction_handler import PredictionHandler

filename = "../datasets/germandata-gender.csv"
outcome_name = "credit_score"
test_size = 0.25
dataset_handler = DatasetHandler(filename, outcome_name, test_size)

attributes_train, outcomes_train = dataset_handler.get_training_dataset()
attributes_test, outcomes_test = dataset_handler.get_testing_dataset()
print("ATTRIBUTES_TRAIN: ", attributes_train)
print("ATTRIBUTES_TEST: ", attributes_test)
print("OUTCOMES_TRAIN: ", outcomes_train)
print("OUTCOMES_TEST: ", outcomes_test)

decision_algorithm = Creator().factory_method("fair_classifier", attributes_train, outcomes_train)

attributes_test, outcomes_test = dataset_handler.get_testing_dataset()
prediction_handler = PredictionHandler(decision_algorithm, attributes_test)

attributes_values = dataset_handler.get_attributes_values()
descriptions = get_descriptions({'personal_status_and_gender': attributes_values["personal_status_and_gender"]})
for description in descriptions:
    print(description)

calculator = FairnessDefinitionsCalculator(prediction_handler, dataset_handler, descriptions)
calculator.calculate_all({})

"""
required_parameters = calculator.get_required_parameters_names()
print(required_parameters)
required_parameters_values = dict()
for parameter in required_parameters:
    print(parameter)
    required_parameters_values[parameter] = input()
calculator.calculate_all(required_parameters_values)
"""

"""
from [app].models import *
all you will need to do is

klass = globals()["class_name"]
instance = klass()
"""