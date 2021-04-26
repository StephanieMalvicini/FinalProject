class ValueAlreadyExists(Exception):

    def __init__(self, repeated_name, repeated_value):
        self.title = "No se puede añadir el clasificador/algoritmo de decisión"
        self.message = "Ya existe una entrada con {} = {}".format(repeated_name, repeated_value)
        super().__init__(self.message)
