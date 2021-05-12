import sqlite3

from entities.decision_algorithm import DecisionAlgorithm
from exceptions.decision_algorithm import ValueAlreadyExists

PATH_DB = "databases/database.db"


def insert(decision_algorithm):
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO decision_algorithms VALUES (?,?,?)", (decision_algorithm.display_name,
                                                                          decision_algorithm.class_name,
                                                                          decision_algorithm.full_path))
        connection.commit()
    except sqlite3.IntegrityError:
        raise ValueAlreadyExists("nombre para mostrar", decision_algorithm.display_name)
    finally:
        connection.close()


def get(display_name):
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM decision_algorithms WHERE display_name=?", (display_name,))
    data = cursor.fetchone()
    connection.close()
    return DecisionAlgorithm(data[0], data[1], data[2])


def get_all():
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM decision_algorithms")
    data_list = cursor.fetchall()
    connection.close()
    all_items = list()
    for data in data_list:
        all_items.append(DecisionAlgorithm(data[0], data[1], data[2]))
    return all_items


def get_all_display_names():
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("SELECT display_name FROM decision_algorithms")
    all_names = cursor.fetchall()
    connection.close()
    return [name[0] for name in all_names]


def delete(display_name):
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    cursor.execute("DELETE from decision_algorithms WHERE display_name=?", (display_name,))
    connection.commit()
    connection.close()
