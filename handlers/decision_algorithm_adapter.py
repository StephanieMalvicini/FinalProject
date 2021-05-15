import pandas as pd


class DecisionAlgorithmAdapter:

    def __init__(self, decision_algorithm, attributes_test):
        self.attributes_test = attributes_test
        self.decision_algorithm = decision_algorithm

    def get_predicted_outcomes(self):
        return self.decision_algorithm.predict_outcome(self.attributes_test)

    def get_predicted_probabilities(self):
        return self.decision_algorithm.predict_probability(self.attributes_test)

    def get_predicted_outcome(self, individual):
        dataframe = pd.DataFrame().append(individual)
        return self.decision_algorithm.predict_outcome(dataframe)[0]

    def predicted_outcome_available(self):
        return hasattr(self.decision_algorithm, "predict_outcome")

    def predicted_probability_available(self):
        return hasattr(self.decision_algorithm, "predict_probability")

    def distances_available(self):
        return hasattr(self.decision_algorithm, "individuals_distance") and \
               hasattr(self.decision_algorithm, "outcomes_distance")

    def get_individuals_distance(self, subject1, subject2):
        return self.decision_algorithm.individuals_distance(subject1, subject2)

    def get_outcomes_distance(self, outcome1, outcome2):
        return self.decision_algorithm.outcomes_distance(outcome1, outcome2)