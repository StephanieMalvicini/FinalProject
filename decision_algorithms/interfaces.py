import pandas


class OutcomePredictor:

    def predict_outcome(self, subjects: pandas.DataFrame):
        raise NotImplementedError


class ProbabilityPredictor:

    def predict_probability(self, subjects: pandas.DataFrame):
        raise NotImplementedError


class DistanceCalculator:

    def individuals_distance(self, subject1: pandas.Series, subject2: pandas.Series):
        raise NotImplementedError

    def outcomes_distance(self, output1, output2):
        raise NotImplementedError
