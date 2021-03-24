from decision_algorithms.decision_algorithm import DecisionAlgorithm


class BiasClassifier(DecisionAlgorithm):

    def predict_outcome(self, subjects):
        outcomes = []
        for index, subject in subjects.iterrows():
            if subject["personal_status_and_gender"] == 0:
                outcomes.append(0)
            else:
                outcomes.append(1)
        return outcomes

    def predict_probability(self, subjects):
        raise NotImplementedError

    def subjects_distance(self, subject1, subject2):
        raise NotImplementedError

    def outcomes_distance(self, output1, output2):
        raise NotImplementedError

