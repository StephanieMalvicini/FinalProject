from decision_algorithms.interfaces import *


class FairClassifier(OutcomePredictor, ProbabilityPredictor, DistanceCalculator):

    def individuals_distance(self, subject1, subject2):
        return 1

    def outcomes_distance(self, output1, output2):
        return 1

    def predict_probability(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(0.9)
        return outcomes

    def predict_outcome(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(1)
        return outcomes


#EDITADO
