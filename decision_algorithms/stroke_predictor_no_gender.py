from sklearn.tree import DecisionTreeClassifier

from decision_algorithms.interfaces import *

dataset_mapping = {
    "Género": {"Masculino": 0, "Femenino": 1, "Otro": 2},
    "Alguna_vez_casadx": {"Sí": 1, "No": 0},
    "Tipo_de_trabajo": {"Privado": 0, "Autónomo": 1, "Gubernamental": 2, "Niñx": 3, "Nunca trabajó": 4},
    "Tipo_de_residencia": {"Urbana": 0, "Rural": 1},
    "Fumador": {"Ex fumador": 0, "Nunca fumó": 1, "Fuma": 2, "Desconocido": 3},
    "Hipertensión": {"Sí": 1, "No": 0},
    "Cardiopatía":  {"Sí": 1, "No": 0}
}


def map_values(dataframe):
    mapped_dataframe = dataframe
    for column in dataset_mapping.keys():
        mapped_dataframe[column] = mapped_dataframe[column].map(dataset_mapping[column])
    try:
        mapped_dataframe = mapped_dataframe.drop("Género")
    except KeyError:
        pass
    return mapped_dataframe


def map_outcome(series):
    return series.map({"Sí": 1, "No": 0})


class StrokePredictor(OutcomePredictor, ProbabilityPredictor, DistanceCalculator):

    def __init__(self, attributes_train, outcomes_train):
        mapped_attributes_train = map_values(attributes_train)
        mapped_outcomes_train = map_outcome(outcomes_train)
        self.model = DecisionTreeClassifier()
        self.model.fit(mapped_attributes_train, mapped_outcomes_train)

    def predict_outcome(self, subjects):
        subjects_copy = subjects.copy(deep=True)
        mapped_subjects = map_values(subjects_copy)
        predictions = self.model.predict(mapped_subjects)
        return ["Sí" if prediction == 1 else "No" for prediction in predictions]

    def predict_probability(self, subjects):
        subjects_copy = subjects.copy(deep=True)
        mapped_subjects = map_values(subjects_copy)
        return self.model.predict_proba(mapped_subjects)[:, 1]

    def individuals_distance(self, subject1: pandas.Series, subject2: pandas.Series):
        differences = 0
        if abs(subject1["Edad"] - subject1["Edad"]) > 5:
            differences += 1
        if subject1["Fumador"] != subject1["Fumador"]:
            differences += 1
        if subject1["Cardiopatía"] != subject1["Cardiopatía"]:
            differences += 1
        if abs(subject1["Nivel_de_glucosa_promedio"] - subject1["Nivel_de_glucosa_promedio"]) > 50:
            differences += 1
        if subject1["Hipertensión"] == subject1["Hipertensión"]:
            differences += 1
        if abs(subject1["IMC"] - subject1["IMC"]) > 5:
            differences += 1
        return differences/6

    def outcomes_distance(self, outcome1, outcome2):
        if outcome1 != outcome2:
            return 1
        else:
            return 0

