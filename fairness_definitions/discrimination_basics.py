import copy
import math

from constants.predictions_names import *


def calculate_basic_metrics(testing_set, descriptions, positive_outcome, negative_outcome):
    metrics = list()
    for _ in range(len(descriptions)):
        metrics.append({"FP": 0, "FN": 0, "TP": 0, "TN": 0})
    for i in range(len(testing_set)):
        description_index = description_individual_satisfies(testing_set.iloc[i], descriptions)
        if description_index >= 0:
            if testing_set.iloc[i][OUTCOME] == negative_outcome and \
                    testing_set.iloc[i][PREDICTED_OUTCOME] == negative_outcome:
                metrics[description_index]["TN"] += 1
            elif testing_set.iloc[i][OUTCOME] == negative_outcome:
                metrics[description_index]["FP"] += 1
            elif testing_set.iloc[i][OUTCOME] == positive_outcome and \
                    testing_set.iloc[i][PREDICTED_OUTCOME] == positive_outcome:
                metrics[description_index]["TP"] += 1
            else:
                metrics[description_index]["FN"] += 1
    return metrics


def description_individual_satisfies(individual, descriptions):
    index = -1
    for i in range(len(descriptions)):
        satisfies = True
        for attribute in descriptions[i].keys():
            if individual[attribute] != descriptions[i][attribute]:
                satisfies = False
                break
        if satisfies:
            index = i
            break
    return index


def create_positives_negatives_tables(testing_set, descriptions, decimals, positive_outcome):
    descriptions_amount = len(descriptions)
    positives_table = list()
    negatives_table = list()
    probabilities_range = create_probabilities_range(decimals)
    for _ in range(descriptions_amount):
        positives_table.append(copy.deepcopy(probabilities_range))
        negatives_table.append(copy.deepcopy(probabilities_range))
    for i in range(len(testing_set)):
        individual = testing_set.iloc[i]
        description_index = description_individual_satisfies(individual, descriptions)
        if description_index >= 0:
            probability = individual[PREDICTED_PROBABILITY]
            s = round(probability, decimals)
            if individual[OUTCOME] == positive_outcome:
                positives_table[description_index][str(s)] += 1
            else:
                negatives_table[description_index][str(s)] += 1
    return positives_table, negatives_table


def create_probabilities_range(decimals):
    probabilities_range = {}
    last = int(math.pow(10, decimals))
    for s in range(0, last + 1):
        probabilities_range[str(s / last)] = 0
    return probabilities_range


def create_probabilities_table(positives_table, negatives_table, decimals):
    subgroups_amount = len(positives_table)
    probabilities_values = positives_table[0].keys()
    probabilities_table = list()
    probabilities_range = create_probabilities_range(decimals)
    for _ in range(subgroups_amount):
        probabilities_table.append(copy.deepcopy(probabilities_range))
    for s in probabilities_values:
        for i in range(subgroups_amount):
            if positives_table[i][s] + negatives_table[i][s] > 0:
                probability = positives_table[i][s] / (positives_table[i][s] + negatives_table[i][s])
            else:
                probability = 0
            probabilities_table[i][s] = probability
    return probabilities_table
