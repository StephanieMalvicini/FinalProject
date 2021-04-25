from random import randrange

from decision_algorithms.interfaces import OutcomePredictor, DistanceCalculator


class BiasClassifier(OutcomePredictor, DistanceCalculator):

    def individuals_distance(self, subject1, subject2):
        return randrange(10)

    def outcomes_distance(self, output1, output2):
        return randrange(10)

    def predict_outcome(self, subjects):
        outcomes = []
        for index, subject in subjects.iterrows():
            if subject["personal_status_and_gender"] == "male":
                outcomes.append(0)
            else:
                outcomes.append(1)
        return outcomes


