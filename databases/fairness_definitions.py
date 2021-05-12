import sqlite3

from entities.fairness_definition import FairnessDefinition

PATH_DB = "databases/database.db"


def get_all():
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fairness_definitions")
    data_list = cursor.fetchall()
    connection.close()
    all_items = list()
    for data in data_list:
        all_items.append(FairnessDefinition(data[0], data[1]))
    return all_items


def get_available_names(outcome_available, predicted_outcome_available, predicted_probability_available,
                        distances_available):
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    conditions = list()
    if not outcome_available:
        conditions.append("outcome=0")
    if not predicted_outcome_available:
        conditions.append("predicted_outcome=0")
    if not predicted_probability_available:
        conditions.append("predicted_probability=0")
    if not distances_available:
        conditions.append("distances=0")
    if len(conditions) == 0:
        cursor.execute("SELECT name, display_name FROM fairness_definitions")
    else:
        cursor.execute("SELECT fairness_definitions.name "
                       "FROM fairness_definitions "
                       "INNER JOIN fairness_definitions_requirements "
                       "ON fairness_definitions.name=fairness_definitions_requirements.name "
                       "WHERE {}".format(" AND ".join(conditions)))
    names = cursor.fetchall()
    connection.close()
    return [name[0] for name in names]
