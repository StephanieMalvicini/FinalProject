from decision_algorithms.decision_algorithm import DecisionAlgorithm


class FairClassifier(DecisionAlgorithm):

    def predict_outcome(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(1)
        return outcomes

    def predict_probability(self, subjects):
        raise NotImplementedError

    def subjects_distance(self, subject1, subject2):
        raise NotImplementedError

    def outputs_distance(self, output1, output2):
        raise NotImplementedError
