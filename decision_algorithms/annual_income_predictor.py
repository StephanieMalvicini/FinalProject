from sklearn.linear_model import LogisticRegression

from decision_algorithms.interfaces import *

dataset_mapping = {
    "Género": {"Masculino": 0, "Femenino": 1},
    "EstadoCivil": {"Solterx": 0, "Casadx": 1, "Separadx": 2, "Divorciadx": 3, "Viudx": 4},
    "TipoEmpleo": {"Autónomo": 0, "Gubernamental": 1, "Otro/Desconocido": 2, "Privado": 3},
    "Educación": {"Preescolar": 0, "1º-4º": 1, "5º-6º": 2, "7º-8º": 3, "9º": 4, "10º": 5, "11º": 6, "12º": 7,
                  "Secundario": 8, "FormaciónProfesional": 9, "Tecnicatura": 10, "UniversitarioIncompleto": 11,
                  "Universitario": 12, "Magíster": 13, "Doctorado": 15},
    "Profesión": {"Oficinista": 0, "Ventas": 1, "Servicio": 2, "Obrero": 3, "Profesional": 4, "Otro/Desconocido": 5},
    "Raza": {"Blancx": 0, "Negrx": 1, "Asiáticx/IsleñxDelPacífico": 2, "Indígena/Esquimal": 3, "Otro": 4}
}


def map_values(dataframe):
    mapped_dataframe = dataframe
    for column in dataset_mapping.keys():
        mapped_dataframe[column] = mapped_dataframe[column].map(dataset_mapping[column])
    try:
        mapped_dataframe = mapped_dataframe.drop("Género")
        mapped_dataframe = mapped_dataframe.drop("Raza")
    except KeyError:
        pass
    return mapped_dataframe


def map_outcome(series):
    return series.map({"50milO-": 0, "+50mil": 1})


class AnnualIncomePredictor(OutcomePredictor, ProbabilityPredictor, DistanceCalculator):

    def __init__(self, attributes_train, outcomes_train):
        mapped_attributes_train = map_values(attributes_train)
        mapped_outcomes_train = map_outcome(outcomes_train)
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(mapped_attributes_train, mapped_outcomes_train)

    def predict_outcome(self, subjects):
        subjects_copy = subjects.copy(deep=True)
        mapped_subjects = map_values(subjects_copy)
        predictions = self.model.predict(mapped_subjects)
        return ["+50mil" if prediction == 1 else "50milO-" for prediction in predictions]

    def predict_probability(self, subjects):
        subjects_copy = subjects.copy(deep=True)
        mapped_subjects = map_values(subjects_copy)
        return self.model.predict_proba(mapped_subjects)[:, 1]

    def individuals_distance(self, subject1: pandas.Series, subject2: pandas.Series):
        same_attributes = subject1.drop(columns=["Género", "Raza"]).equals(subject2.drop(columns=["Género", "Raza"]))
        if same_attributes:
            return 0
        return 1

    def outcomes_distance(self, outcome1, outcome2):
        if outcome1 != outcome2:
            return 1
        else:
            return 0

