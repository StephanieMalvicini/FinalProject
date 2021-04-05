from decision_algorithms.interfaces import OutcomePredictor


class FairClassifier(OutcomePredictor):

    def predict_outcome(self, subjects):
        outcomes = []
        for _ in subjects.iterrows():
            outcomes.append(1)
        return outcomes
