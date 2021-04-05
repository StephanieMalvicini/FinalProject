class OutcomePredictor:

    def predict_outcome(self, subjects):
        raise NotImplementedError


class ProbabilityPredictor:

    def predict_probability(self, subjects):
        raise NotImplementedError


class DistanceCalculator:

    def individuals_distance(self, subject1, subject2):
        raise NotImplementedError

    def outcomes_distance(self, output1, output2):
        raise NotImplementedError

