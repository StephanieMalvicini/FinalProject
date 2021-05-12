from handlers.results import SingleElement, TableElement, ListElement


class ParametersResult:

    def __init__(self, all_parameters):
        self.display_names = dict((param.name, param.display_name) for param in all_parameters)
        self.display_names["percentage"] = "Porcentaje que no satisface"
        self.display_names["test_suite"] = "Conjunto de pruebas"
        self.display_names["test_suite_total_cases"] = "Total casos analizados"
        self.display_names["predicted_outcome"] = "SalidaPredicha"
        self.display_names["predicted_probability"] = "ProbabilidadPredicha"
        self.display_names["confidence_reached"] = "alcanzada"
        self.display_names["confidence_not_reached"] = "no alcanzada"
        self.display_names["failing_cases"] = "Casos donde falla"
        self.display_names["satisfies"] = "Satisface"
        self.display_names["not_satisfies"] = "No satisface"
        self.display_names["result"] = "Resultado"
        self.display_names["probabilities_table"] = "Tabla probabilidades"
        self.display_names["expected_values"] = "Valores esperados"

    def predicted_outcome_display_name(self):
        return self.display_names["predicted_outcome"]

    def predicted_probability_display_name(self):
        return self.display_names["predicted_probability"]

    def add_confidence(self, result, value, confidence_reached):
        if confidence_reached:
            detail = self.display_names["confidence_reached"]
        else:
            detail = self.display_names["confidence_not_reached"]
        result.add_element(SingleElement(self.display_names["confidence"], "{}% ({})".format(value, detail)))

    def add_minimum_samples_amount(self, result, value):
        result.add_element(SingleElement(self.display_names["minimum_samples_amount"], value))

    def add_percentage(self, result, proportion, error):
        result.add_element(SingleElement(self.display_names["percentage"],
                                         "({} ± {})%".format(round(proportion * 100, 2), error)))

    def add_test_suite(self, result, test_suite, descriptions):
        # arrange attributes so the ones used in the descriptions goes first
        sorted_columns = list(descriptions[0].keys())
        sorted_columns.insert(0, "PredictedOutcome")
        for column in test_suite.columns:
            if column not in sorted_columns:
                sorted_columns.append(column)
        testing_suite = test_suite[sorted_columns]
        testing_suite.rename(columns={"PredictedOutcome": self.display_names["predicted_outcome"]})
        column_names = list(testing_suite.columns)
        data = testing_suite.values.tolist()
        result.add_element(TableElement(self.display_names["test_suite"], column_names, data))
        result.add_element(SingleElement(self.display_names["test_suite_total_cases"], len(data)))

    def add_maximum_acceptable_difference(self, result, value):
        result.add_element(SingleElement(self.display_names["maximum_acceptable_difference"], value))

    def add_failing_cases(self, result, failing_cases):
        result.add_element(SingleElement(self.display_names["failing_cases"], len(failing_cases)))
        """for case in failing_cases:
            result.add_element(SingleElement("Sujeto 1", format_descriptions(case.individual1.to_dict())))
            result.add_element(SingleElement("Sujeto 2", format_descriptions(case.individual2.to_dict())))
            result.add_element(SingleElement("Distancia entre sujetos", case.individuals_distance))
            result.add_element(SingleElement("Distancia entre salidas", case.outcomes_distance))
        """

    def add_probabilities_table(self, result, template, column_satisfies, descriptions, probabilities_table):
        row_descriptions = list()
        for description in descriptions:
            formatted_description = format_description(description)
            row_descriptions.append(template.format(formatted_description))
        column_names = list(probabilities_table[0].keys())
        column_names.insert(0, "s")
        data = [list(dict_probabilities.values()) for dict_probabilities in probabilities_table]
        for i, row in enumerate(data):
            row.insert(0, row_descriptions[i])
        results_row = [self.display_names["satisfies"] if element else self.display_names["not_satisfies"]
                       for element in column_satisfies.values()]
        results_row.insert(0, self.display_names["result"])
        data.append(results_row)
        result.add_element(TableElement(self.display_names["probabilities_table"], column_names, data, False))

    def add_decimals(self, result, value):
        result.add_element(SingleElement(self.display_names["decimals"], value))

    def add_list(self, result, list_name, list_values, template, descriptions):
        if list_name in self.display_names.keys():
            list_name = self.display_names[list_name]
        formatted_descriptions = [format_description(description) for description in descriptions]
        items_names = [template.format(description) for description in formatted_descriptions]
        result.add_element(ListElement(list_name, items_names, list_values))

    def add_legitimate_attributes(self, result, legitimate_attributes, list_values, template, descriptions):
        list_name = legitimate_attributes.split(" & ")
        list_name = [item[1:-1] for item in list_name]
        list_name = ",".join(list_name)
        list_name = "L: {}".format(list_name)
        self.add_list(result, list_name, list_values, template, descriptions)


def format_description(description):
    formatted_descriptions = ["{}={}".format(name, value) for name, value in description.items()]
    formatted_descriptions = ",".join(formatted_descriptions)
    return formatted_descriptions
