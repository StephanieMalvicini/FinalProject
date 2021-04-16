import importlib
import sys

import pandas as pd

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters

DECISION_ALGORITHMS_FILENAME = "decision_algorithms/decision_algorithms.csv"


class DecisionAlgorithmHandler:

    def __init__(self):
        self.decision_algorithms = pd.read_csv(DECISION_ALGORITHMS_FILENAME)

    def get_decision_algorithms_names(self):
        return list(self.decision_algorithms["display_name"])

    def create_decision_algorithm(self, display_name, *decision_algorithm_params):
        decision_algorithm = self.decision_algorithms.loc[self.decision_algorithms["display_name"] == display_name].iloc[0]
        class_name = decision_algorithm["class_name"]
        file_name = decision_algorithm["file_name"]
        module = importlib.import_module("decision_algorithms.{}".format(file_name))
        decision_algorithm = getattr(module, class_name)
        try:
            return decision_algorithm(*decision_algorithm_params)
        except TypeError:
            try:
                return decision_algorithm()
            except Exception:
                raise InvalidDecisionAlgorithmParameters(sys.exc_info())
        except Exception:
            raise InvalidDecisionAlgorithmParameters(sys.exc_info())
