import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.style.use("seaborn-pastel")


def create_table_subplot(axis, table, table_title):
    x = [float(value) for value in table[0].keys()]
    for i, group in enumerate(table, start=1):
        axis.plot(x, group.values(), label="Grupo: {}".format(i))
    axis.set_title(table_title)
    axis.legend()
    axis.set_xlabel("Probabilidad predicha")
    axis.set_ylabel("Cantidad")


class Plots:

    def __init__(self, dialog, descriptions, basic_metrics, positives_table, negatives_table):
        self.dialog = dialog
        self.descriptions = descriptions
        self.basic_metrics = basic_metrics
        self.positives_table = positives_table
        self.negatives_table = negatives_table

    def show_basic_metrics(self):
        figure, axis = plt.subplots()
        groups = ["Grupo {}".format(i) for i in range(1, len(self.descriptions) + 1)]
        tp = np.array([metric["TP"] for metric in self.basic_metrics])
        tn = np.array([metric["TN"] for metric in self.basic_metrics])
        fp = np.array([metric["FP"] for metric in self.basic_metrics])
        fn = np.array([metric["FN"] for metric in self.basic_metrics])
        axis.bar(groups, tp)
        axis.bar(groups, tn, bottom=tp)
        axis.bar(groups, fp, bottom=tp+tn)
        axis.bar(groups, fn, bottom=tp+tn+fp)
        axis.legend(["TP", "TN", "FP", "FN"])
        self.dialog.show_plot_with_details("Métricas básicas", figure, "Mostrar descripciones de grupos",
                                           self.get_groups_descriptions(), "Descripciones de grupos")
        plt.close("all")  # so the program can finish, otherwise, it continues executing if the dialog was opened

    def get_groups_descriptions(self):
        names = list()
        for i, description in enumerate(self.descriptions, start=1):
            name = ["{}={}".format(name, value) for name, value in description.items()]
            name = ", ".join(name)
            names.append("Grupo {}: {}".format(i, name))
        return names

    def show_positives_negatives_tables(self):
        figure, (axis1, axis2) = plt.subplots(nrows=1, ncols=2, sharey="True")
        create_table_subplot(axis1, self.positives_table, "Tabla positivos")
        create_table_subplot(axis2, self.negatives_table, "Tabla negativos")
        self.dialog.show_plot_with_details("Cantidades probabilidades predichas", figure,
                                           "Mostrar descripciones de grupos", self.get_groups_descriptions(),
                                           "Descripciones de grupos")
        plt.close("all")  # so the program can finish, otherwise, it continues executing if the dialog was opened

    def has_basic_metrics_plot(self):
        if self.basic_metrics:
            return True
        return False

    def has_positives_negatives_tables_plot(self):
        if self.positives_table and self.negatives_table:
            return True
        return False
