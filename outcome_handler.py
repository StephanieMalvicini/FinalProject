import pandas as pd


class OutcomeHandler:

    def __init__(self):
        self.filename = None
        self.dataset = None
        self.outcome_name = ""
        self.positive_outcome = None
        self.negative_outcome = None

    def update_filename(self, new_filename):
        self.filename = new_filename
        self.dataset = pd.read_csv(new_filename, header=0)

    def get_all_possible_outcomes(self):
        attributes = list(self.dataset.columns)
        possible_outcomes = list()
        for attribute in attributes:
            if len(self.dataset[attribute].unique()) == 2:
                possible_outcomes.append(attribute)
        return possible_outcomes

    def set_outcome_name(self, outcome_name):
        self.outcome_name = outcome_name

    def get_outcome_values(self):
        return list(self.dataset[self.outcome_name].unique())

    def set_outcome_values(self, positive_outcome_value):
        if positive_outcome_value is None:
            self.negative_outcome = None
            self.positive_outcome = None
        else:
            outcome_values = self.get_outcome_values()
            if str(positive_outcome_value) == str(outcome_values[0]):
                self.positive_outcome = outcome_values[0]
                self.negative_outcome = outcome_values[1]
            else:
                self.positive_outcome = outcome_values[1]
                self.negative_outcome = outcome_values[0]
