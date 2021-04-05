from decision_algorithms.interfaces import OutcomePredictor


class BiasClassifier(OutcomePredictor):

    def predict_outcome(self, subjects):
        outcomes = []
        for index, subject in subjects.iterrows():
            if subject["personal_status_and_gender"] == 0:
                outcomes.append(0)
            else:
                outcomes.append(1)
        return outcomes

