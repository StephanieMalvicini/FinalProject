import importlib
import os
import sys

from databases import decision_algorithms
from exceptions.decision_algorithm import InvalidDecisionAlgorithmParameters, InvalidModuleName


def get(display_name, decision_algorithm_params):
    decision_algorithm = decision_algorithms.get(display_name)
    file_name = os.path.basename(decision_algorithm.full_path)
    sys.path.insert(1, decision_algorithm.full_path[0:-len(file_name)])
    try:
        module = importlib.import_module(file_name[0:-3])
    except ModuleNotFoundError:
        raise InvalidModuleName()
    decision_algorithm_class = getattr(module, decision_algorithm.class_name)
    try:
        return decision_algorithm_class(*decision_algorithm_params)
    except TypeError:
        try:
            return decision_algorithm_class()
        except Exception:
            raise InvalidDecisionAlgorithmParameters(sys.exc_info())
    except Exception:
        raise InvalidDecisionAlgorithmParameters(sys.exc_info())
