import sqlite3

from entities.parameter import Parameter, ParameterType

PATH_DB = "databases/database.db"


def get_all():
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT name, display_name FROM parameters")
    data_list = cursor.fetchall()
    connection.close()
    all_items = list()
    for data in data_list:
        all_items.append(Parameter(data[0], data[1]))
    return all_items


def get_required_names(fairness_definitions_names):
    if len(fairness_definitions_names) == 0:
        return list()
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT parameters.name "
                   "FROM parameters "
                   "INNER JOIN fairness_definitions_parameters "
                   "ON parameters.name=fairness_definitions_parameters.parameter "
                   "WHERE fairness_definitions_parameters.name "
                   "IN ({})".format(",".join(["?"]*len(fairness_definitions_names))), fairness_definitions_names)
    names = cursor.fetchall()
    connection.close()
    return [name[0] for name in names]


def get_types(parameters_names):
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT name, type FROM parameters WHERE name IN ({})"
                   .format(",".join(["?"]*len(parameters_names))), parameters_names)
    data_list = cursor.fetchall()
    connection.close()
    all_items = list()
    for data in data_list:
        all_items.append(ParameterType(data[0], data[1]))
    return all_items
