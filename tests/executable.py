import sys
from decision_algorithms.creator import Creator


decision_algorithm = Creator().factory_method(decision_algorithm_name="logistic_regression_classifier")
subject = sys.argv[1:]
subject = [int(i) for i in subject]
print(int(decision_algorithm.predict_outcome([tuple(subject)])[0]))


