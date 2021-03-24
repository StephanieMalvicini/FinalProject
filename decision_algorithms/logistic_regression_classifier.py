from sklearn.linear_model import LogisticRegression
from decision_algorithms.decision_algorithm import DecisionAlgorithm


class LogisticRegressionClassifier(DecisionAlgorithm):

    def __init__(self, attributes_train, outcomes_train):
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(attributes_train, outcomes_train)

    def predict_outcome(self, subjects):
        result = self.model.predict(subjects)
        return result

    def predict_probability(self, subjects):
        return self.model.predict_proba(subjects)

    def subjects_distance(self, subject1, subject2):
        raise NotImplementedError

    def outcomes_distance(self, output1, output2):
        raise NotImplementedError

