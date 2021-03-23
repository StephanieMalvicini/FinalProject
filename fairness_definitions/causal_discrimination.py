import copy
import math
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

conf_zValue = {80: 1.28, 90: 1.645, 95: 1.96, 98: 2.33, 99: 2.58}


def causal_discrimination(testing_set, descriptions, confidence, error, minimum_samples_amount, decision_algorithm):
    fails_amount = 0
    test_suite = pd.DataFrame()
    samples_amount = 0
    for i in range(len(testing_set.index)):
        individual = testing_set.iloc[i]
        if not (test_suite == individual).all(1).any():
            samples_amount += 1
            test_suite = test_suite.append(individual, ignore_index=True)
            fails = False
            for description in descriptions:
                similar_individual = create_similar_individual(individual, description)
                if not similar_individual.equals(individual):
                    del similar_individual["PredictedOutcome"]
                    # subject = [int(i) for i in similar_individual.values()]
                    # print("ACAAAAAAAAAA", subject, "AAAAAAAAAAA")
                    # similar_individual["PredictedOutcome"] = decision_algorithm.predict_outcome([tuple(subject)])
                    similar_individual["PredictedOutcome"] = decision_algorithm.predict_outcome(pd.DataFrame().append(similar_individual))[0]
                    # similar_individual["PredictedOutcome"] = decision_algorithm.predict_outcome([
                    # similar_individual])[0]
                    test_suite = test_suite.append(similar_individual, ignore_index=True)
                    if similar_individual["PredictedOutcome"] != individual["PredictedOutcome"]:
                        fails = True
            if fails:
                fails_amount += 1
            if samples_amount > minimum_samples_amount:
                p = fails_amount / samples_amount
                current_error = conf_zValue[int(100 * confidence)] * math.sqrt(p * (1 - p) * 1.0 / samples_amount)
                if current_error < error:
                    break
    print(test_suite.to_string())
    print("fails_amount: ", fails_amount)
    print("samples_amount: ", samples_amount)
    return fails_amount / samples_amount # por si nunca llega a tener mas ejemplos de los requeridos


def create_similar_individual(individual, description) -> object:
    similar_individual = copy.deepcopy(individual)
    for attribute in description.keys():
        similar_individual[attribute] = description[attribute]
    return similar_individual
