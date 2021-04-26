class InvalidDecisionAlgorithmParameters(Exception):

    def __init__(self, original_error):
        self.original_error = original_error
        self.message = "Parece que el conjunto de datos no se corresponde con los requerimientos del " \
                       "clasificador/algoritmo de decisión "
        super().__init__(self.message)
