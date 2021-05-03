import pandas as pd

FAIRNESS_DEFINITIONS_FILENAME = "fairness_definitions/fairness_definitions.csv"
PARAMETERS_FILENAME = "fairness_definitions/fairness_definitions_parameters.csv"


class FairnessDefinitionsParametersHandler:

    def __init__(self, prediction_handler, dataset_handler):
        self.definitions = pd.read_csv(FAIRNESS_DEFINITIONS_FILENAME)
        self.parameters = pd.read_csv(PARAMETERS_FILENAME)
        self.available_definitions = self.__get_available_definitions(prediction_handler, dataset_handler)
        self.required_parameters = self.__get_required_parameters(self.available_definitions)

    def __get_available_definitions(self, prediction_handler, dataset_handler):
        requirements = list()
        if not prediction_handler.predicted_outcome_available():
            requirements.append("predicted_outcome != 'required'")
        if not prediction_handler.predicted_probability_available():
            requirements.append("predicted_probability != 'required'")
        if not prediction_handler.distances_available():
            requirements.append("distances != 'required'")
        if not dataset_handler.has_outcome():
            requirements.append("outcome != 'required'")
        all_requirements = " & ".join(requirements)
        if len(all_requirements) == 0:
            return self.definitions
        return self.definitions[self.definitions.eval(all_requirements)]

    def __get_required_parameters(self, definitions):
        parameters_filter = list()
        for parameter in self.parameters["parameter_name"]:
            parameters_filter.append("required" in definitions[parameter].unique())
        return self.parameters[parameters_filter]

    def get_required_parameters_names(self, definitions_names):
        definitions_filer = list()
        for name in self.available_definitions["definition_name"]:
            definitions_filer.append(name in definitions_names)
        definitions = self.available_definitions[definitions_filer]
        return list(self.__get_required_parameters(definitions)["parameter_name"])

    def get_available_definitions_names(self):
        return list(self.available_definitions["definition_name"])

    def get_all_definitions_displays_names(self):
        return pd.Series(self.definitions.display_name.values, index=self.definitions.definition_name).to_dict()

    def get_all_required_parameters_names(self):
        return list(self.required_parameters["parameter_name"])

    def get_all_parameters_display_names(self):
        return pd.Series(self.parameters.display_name.values, index=self.parameters.parameter_name).to_dict()

    def transform_parameters_type(self, parameters_values):
        for name, value in parameters_values.items():
            parameter = self.required_parameters.loc[self.required_parameters["parameter_name"] == name]
            if "yes" in parameter["float"].unique():
                parameters_values[name] = float(value)
            elif "yes" in parameter["int"].unique():
                parameters_values[name] = int(value)
