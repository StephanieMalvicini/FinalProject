class DecisionAlgorithm:

    def predict_outcome(self, subjects):
        raise NotImplementedError

    def predict_probability(self, subjects):
        raise NotImplementedError

    def subjects_distance(self, subject1, subject2):
        raise NotImplementedError

    def outcomes_distance(self, output1, output2):
        raise NotImplementedError


# el predict recibe un sujeto asi: [(6,148,72,35,0,33.6,0.627,50)]