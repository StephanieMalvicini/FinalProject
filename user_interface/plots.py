import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

COLORS = ["#92C6FF", "#97F0AA", "#FF9F9A", "#D0BBFF", "#FFFEA3", "#B0E0E6",
          "#94b2ff", "#b0f098", "#ff99ce", "#f6bdff", "#ffe2a3", "#b1e7da"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=COLORS)


class PlotsDisplayNames:

    def __init__(self):
        self.group = "Grupo"
        self.basic_metrics = "Métricas básicas"
        self.show_groups_descriptions = "Mostrar descripciones de grupos"
        self.groups_descriptions = "Descripciones de grupos"
        self.positives_table = "Tabla positivos"
        self.negatives_table = "Tabla negativos"
        self.predicted_probabilities_amount = "Cantidades probabilidades predichas"
        self.predicted_probability = "Probabilidad predicha"
        self.amount = "Cantidad"


class Plots:

    def __init__(self, dialog, descriptions, basic_metrics, positives_table, negatives_table):
        self.dialog = dialog
        self.descriptions = descriptions
        self.basic_metrics = basic_metrics
        self.positives_table = positives_table
        self.negatives_table = negatives_table
        self.display_names = PlotsDisplayNames()

    def show_basic_metrics(self):
        figure, axis = plt.subplots()
        groups = ["{} {}".format(self.display_names.group, i) for i in range(1, len(self.descriptions) + 1)]
        tp = np.array([metric["TP"] for metric in self.basic_metrics])
        tn = np.array([metric["TN"] for metric in self.basic_metrics])
        fp = np.array([metric["FP"] for metric in self.basic_metrics])
        fn = np.array([metric["FN"] for metric in self.basic_metrics])
        axis.bar(groups, tp)
        axis.bar(groups, tn, bottom=tp)
        axis.bar(groups, fp, bottom=tp+tn)
        axis.bar(groups, fn, bottom=tp+tn+fp)
        axis.legend(["TP", "TN", "FP", "FN"])
        self.dialog.show_plot_with_details(self.display_names.basic_metrics,
                                           figure,
                                           self.display_names.show_groups_descriptions,
                                           self.get_groups_descriptions(),
                                           self.display_names.groups_descriptions)
        plt.close("all")  # so the program can finish, otherwise, it continues executing if the dialog was opened

    def get_groups_descriptions(self):
        names = list()
        for i, description in enumerate(self.descriptions, start=1):
            name = ["{}={}".format(name, value) for name, value in description.items()]
            name = ", ".join(name)
            names.append("{} {}: {}".format(self.display_names.group, i, name))
        return names

    def show_positives_negatives_tables(self):
        figure, (axis1, axis2) = plt.subplots(nrows=1, ncols=2, sharey="all")
        self.create_table_subplot(axis1, self.positives_table, self.display_names.positives_table)
        self.create_table_subplot(axis2, self.negatives_table, self.display_names.negatives_table)
        self.dialog.show_plot_with_details(self.display_names.predicted_probabilities_amount,
                                           figure,
                                           self.display_names.show_groups_descriptions,
                                           self.get_groups_descriptions(),
                                           self.display_names.groups_descriptions,
                                           with_colors=True)
        plt.close("all")  # so the program can finish, otherwise, it continues executing if the dialog was opened

    def create_table_subplot(self, axis, table, table_title):
        x = [float(value) for value in table[0].keys()]
        for i, group in enumerate(table, start=1):
            axis.plot(x, group.values(), label="{}: {}".format(self.display_names.group, i), marker="o")
        axis.set_title(table_title)
        axis.legend()
        axis.set_xlabel(self.display_names.predicted_probability)
        axis.set_ylabel(self.display_names.amount)

    def has_basic_metrics_plot(self):
        if self.basic_metrics:
            return True
        return False

    def has_positives_negatives_tables_plot(self):
        if self.positives_table and self.negatives_table:
            return True
        return False
