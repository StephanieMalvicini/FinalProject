class InvalidDecisionAlgorithmFile(Exception):

    def __init__(self):
        self.message = "El archivo seleccionado no contiene una clase válida"
        super().__init__(self.message)
