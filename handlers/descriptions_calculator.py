from itertools import product


def get(selected_attributes):
    combinations = product(*selected_attributes.values())
    descriptions = list()
    for combination in combinations:
        description = dict()
        for i, attribute in enumerate(selected_attributes.keys()):
            description[attribute] = combination[i]
        descriptions.append(description)
    return descriptions

