import random
import xml.etree.ElementTree as ET
import themis.themis as themis


def load_soft_from_settings():
    names = []
    types = []
    values = []
    num_values = []

    tree = ET.parse('settings.xml')
    root = tree.getroot()

    command = "python2 loan.py"
    inputs = root.find("inputs")

    for uid, obj in enumerate(inputs.findall("input")):
        names.append(obj.find("name").text)
        types.append(obj.find("type").text)
        if types[uid] == "categorical":
            values.append([elt.text for elt in obj.find("values").findall("value")])
        elif types[uid] == "continuousInt":
            values.append(range(int(obj.find("bounds").find("lowerbound").text),
                                int(obj.find("bounds").find("upperbound").text)))
        else:
            assert False
        num_values.append(len(values[uid]))

    print(names)
    print(values)
    print(num_values)
    print(command)
    print(types)

    return themis.soft(names, values, num_values, command, types)


if __name__ == '__main__':
    soft = load_soft_from_settings()
    soft.printSoftwareDetails()
    D = soft.discriminationSearch(0.2, 0.99, 0.1, "groupandcausal")

    print("\n\n\nThemis has completed \n")
    print("Software discriminates against ", D)
    X = [1]
    print("Group discrimination: ", soft.groupDiscrimination(X, 0.99, 0.1), "\n")
    print("Causal discrimination: ", soft.causalDiscrimination(X, 0.99, 0.1), "\n")
    print("Test suite: ", soft.getTestSuite())
