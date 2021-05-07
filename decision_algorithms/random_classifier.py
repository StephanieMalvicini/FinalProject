from random import randrange, randint, uniform

from decision_algorithms.interfaces import *


class RandomClassifier(OutcomePredictor, DistanceCalculator, ProbabilityPredictor):

    def predict_probability(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(uniform(0, 1))
        return outcomes

    def individuals_distance(self, subject1, subject2):
        return randrange(5)

    def outcomes_distance(self, output1, output2):
        return randrange(5)

    def predict_outcome(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(randint(0, 1))
        return outcomes


