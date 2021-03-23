import copy
import math


def basic_metrics_calculator(testing_set, descriptions):
    metrics = list()
    for _ in range(len(descriptions)):
        metrics.append({"FP": 0, "FN": 0, "TP": 0, "TN": 0})
    for i in range(len(testing_set)):
        description_index = description_individual_satisfies(testing_set.iloc[i], descriptions)
        if description_index >= 0:
            if testing_set.iloc[i]["Outcome"] == 0 and testing_set.iloc[i]["PredictedOutcome"] == 0:
                metrics[description_index]["TN"] += 1
            elif testing_set.iloc[i]["Outcome"] == 0:
                metrics[description_index]["FP"] += 1
            elif testing_set.iloc[i]["Outcome"] == 1 and testing_set.iloc[i]["PredictedOutcome"] == 1:
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


def probability_tables_calculator(testing_set, descriptions, decimals):
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
            probability = individual["PredictedProbability"]
            s = round(probability, decimals)
            if individual["Outcome"] == 1:
                positives_table[description_index][str(s)] += 1
            else:
                negatives_table[description_index][str(s)] += 1
    return positives_table, negatives_table


def create_probabilities_range(decimals):
    probabilities_range = {}
    last = int(math.pow(10, decimals))
    for s in range(0, last+1):
        probabilities_range[str(s/last)] = 0
    return probabilities_range
