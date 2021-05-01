import csv
import importlib
import os
import sys

import pandas as pd

from exceptions.invalid_decision_algorithm_parameters import InvalidDecisionAlgorithmParameters
from exceptions.value_already_exists import ValueAlreadyExists

DECISION_ALGORITHMS_FILENAME = "decision_algorithms/decision_algorithms.csv"


class DecisionAlgorithmHandler:

    def __init__(self):
        self.decision_algorithms = pd.read_csv(DECISION_ALGORITHMS_FILENAME)

    def get_decision_algorithms_names(self):
        return list(self.decision_algorithms["display_name"])

    def get_decision_algorithms(self):
        return self.decision_algorithms.T.to_dict().values()

    def create_decision_algorithm(self, display_name, *decision_algorithm_params):
        decision_algorithm = self.decision_algorithms.loc[self.decision_algorithms["display_name"] == display_name].iloc[0]
        class_name = decision_algorithm["class_name"]
        full_path = decision_algorithm["full_path"]
        file_name = os.path.basename(full_path)
        sys.path.insert(1, full_path[0:-len(file_name)])
        module = importlib.import_module(file_name[0:-3])
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

    def add_decision_algorithm(self, row):
        if row["display_name"] in self.decision_algorithms["display_name"].unique():
            raise ValueAlreadyExists("nombre para mostrar", row["display_name"])
        with open(DECISION_ALGORITHMS_FILENAME, "a+", newline="") as dw:
            writer = csv.DictWriter(dw, fieldnames=row.keys())
            writer.writerow(row)
        self.decision_algorithms = self.decision_algorithms.append(row, ignore_index=True)

    def delete_decision_algorithm(self, display_name):
        self.decision_algorithms = self.decision_algorithms[self.decision_algorithms.display_name != display_name]
        self.decision_algorithms.to_csv(DECISION_ALGORITHMS_FILENAME, index=False)
