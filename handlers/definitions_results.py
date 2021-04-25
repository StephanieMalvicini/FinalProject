from user_interface.definitions_results import *


class Result:

    def __init__(self, satisfies):
        self.elements = list()
        self.satisfies = satisfies

    def add_element(self, element):
        self.elements.append(element)

    def show(self, frame):
        show_result(self.satisfies, frame)
        for element in self.elements:
            element.show(frame)


class ListElement:

    def __init__(self, name, items_names, items):
        self.name = name
        self.items_names = items_names
        self.items = items

    def show(self, frame):
        show_list_element(self, frame)


class TableElement:

    def __init__(self, name, column_names, data):
        self.name = name
        self.column_names = column_names
        self.data = data

    def show(self, frame):
        show_table_element(self, frame)


class SingleElement:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def show(self, frame):
        show_single_element(self, frame)


"""
class ListOfResults:
    
    def __init__(self):
        self.results = list()
        self.all_satisfy = True

    def add_element(self, result):
        self.results.append(result)
        self.all_satisfy &= result.satisfies

    def show(self, frame):
        for result in self.results:
            result.show(frame)
"""
