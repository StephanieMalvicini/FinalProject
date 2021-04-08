import copy
import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetHandler:

    def __init__(self, filename, outcome_name, test_size):
        self.__dataset = pd.read_csv(filename, header=0)
        self.outcome_name = outcome_name
        self.__attributes_train, self.__attributes_test, self.__outcomes_train, self.__outcomes_test = \
            self.__get_train_test_dataset(test_size)

    def __get_train_test_dataset(self, test_size):
        attributes_train = pd.DataFrame()
        outcomes_train = pd.DataFrame()
        column_names = self.__dataset.columns
        if self.has_outcome():
            column_names.drop(self.outcome_name)
            outcomes = self.__dataset[self.outcome_name]
        else:
            outcomes = pd.DataFrame()
        attributes = self.__dataset[column_names]
        outcomes_test = outcomes
        if test_size == 1:
            attributes_test = attributes
        else:
            if self.has_outcome():
                attributes_train, attributes_test, outcomes_train, outcomes_test = \
                    train_test_split(attributes, outcomes, test_size=test_size, random_state=0)
            else:
                attributes_train, attributes_test = \
                    train_test_split(attributes, test_size=test_size, random_state=0)
        return attributes_train, attributes_test, outcomes_train, outcomes_test

    def get_training_dataset(self):
        return copy.deepcopy(self.__attributes_train), copy.deepcopy(self.__outcomes_train)

    def get_testing_dataset(self):
        return copy.deepcopy(self.__attributes_test), copy.deepcopy(self.__outcomes_test)

    def get_attributes_values(self):
        attributes_names = self.__dataset.columns
        if self.has_outcome():
            attributes_names.drop(self.outcome_name)
        attributes_values = dict()
        for attribute in attributes_names:
            attributes_values[attribute] = self.__dataset[attribute].unique()
        return attributes_values

    def has_outcome(self):
        return self.outcome_name != ""

    def get_testing_dataset_samples_amount(self):
        return len(self.__attributes_test)