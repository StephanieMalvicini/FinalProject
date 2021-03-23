from __future__ import annotations

from decision_algorithms.bias_classifier import BiasClassifier
from decision_algorithms.decision_algorithm import DecisionAlgorithm
from decision_algorithms.fair_classifier import FairClassifier
from decision_algorithms.logistic_regression_classifier import LogisticRegressionClassifier


class Creator:
    """
    The Creator class declares the factory method that is supposed to return an
    object of a Product class. The Creator's subclasses usually provide the
    implementation of this method.
    """

    _decision_algorithm = None

    def factory_method(self, decision_algorithm_name, *training_data) -> DecisionAlgorithm:
        if self._decision_algorithm is None:
            if decision_algorithm_name == "logistic_regression_classifier":
                self._decision_algorithm = LogisticRegressionClassifier(training_data[0], training_data[1])
            elif decision_algorithm_name == "bias_classifier":
                self._decision_algorithm = BiasClassifier()
            elif decision_algorithm_name == "fair_classifier":
                self._decision_algorithm = FairClassifier()
        return self._decision_algorithm




