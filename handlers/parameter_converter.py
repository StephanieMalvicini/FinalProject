from databases import parameters


def transform_parameters_type(parameters_values):
    parameters_types = parameters.get_types(list(parameters_values.keys()))
    for parameter in parameters_types:
        if parameter.name in parameters_values.keys():
            if parameter.type == "int":
                parameters_values[parameter.name] = int(parameters_values[parameter.name])
            elif parameter.type == "float":
                parameters_values[parameter.name] = float(parameters_values[parameter.name])
