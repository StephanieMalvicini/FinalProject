class InvalidDecisionAlgorithmFile(Exception):

    def __init__(self):
        self.message = "El archivo seleccionado no contiene una clase válida"
        super().__init__(self.message)


class InvalidDecisionAlgorithmParameters(Exception):

    def __init__(self, original_error):
        self.original_error = original_error
        self.message = "Parece que el conjunto de datos no se corresponde con los requerimientos del " \
                       "clasificador/algoritmo de decisión "
        super().__init__(self.message)


class ValueAlreadyExists(Exception):

    def __init__(self, repeated_name, repeated_value):
        self.title = "No se puede añadir el clasificador/algoritmo de decisión"
        self.message = "Ya existe una entrada con {} = {}".format(repeated_name, repeated_value)
        super().__init__(self.message)


class InvalidModuleName(Exception):
    def __init__(self):
        self.title = "Clasificador/algoritmo de decisión inválido"
        self.message = "Parece que el archivo no existe o fue movido"
        super().__init__(self.message)
