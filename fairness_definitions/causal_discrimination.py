import copy
import math
import pandas as pd
import warnings

from constants import statistical_constants
from constants.predictions_names import *

warnings.simplefilter(action='ignore', category=FutureWarning)


def causal_discrimination(attributes_test, descriptions, confidence, error, minimum_samples_amount, predict_outcome):
    testing_set = copy.deepcopy(attributes_test)
    fails_amount = 0
    test_suite = pd.DataFrame()
    samples_amount = 0
    confidence_reached = False
    for i in range(len(testing_set.index)):
        individual = testing_set.iloc[i]
        if not (test_suite == individual).all(1).any():
            samples_amount += 1
            test_suite = test_suite.append(individual, ignore_index=True)
            fails = False
            for description in descriptions:
                similar_individual = create_similar_individual(individual, description)
                if not similar_individual.equals(individual):
                    similar_individual[PREDICTED_OUTCOME] = \
                        predict_outcome(similar_individual)
                    test_suite = test_suite.append(similar_individual, ignore_index=True)
                    if similar_individual[PREDICTED_OUTCOME] != individual[PREDICTED_OUTCOME]:
                        fails = True
            if fails:
                fails_amount += 1
            if samples_amount > minimum_samples_amount:
                p = fails_amount / samples_amount
                current_error = statistical_constants.CONFIDENCE_Z_VALUES[confidence] * math.sqrt(
                    p * (1 - p) / samples_amount)
                if current_error < error:
                    confidence_reached = True
                    break
    return fails_amount / samples_amount, test_suite, confidence_reached


def create_similar_individual(individual, description):
    similar_individual = copy.deepcopy(individual)
    for attribute in description.keys():
        similar_individual[attribute] = description[attribute]
    return similar_individual
