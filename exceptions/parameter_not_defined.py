class ParameterNotDefined(Exception):

    def __init__(self, error_title, error_message):
        self.error_title = error_title
        self.message = error_message
        super().__init__(self.message)
