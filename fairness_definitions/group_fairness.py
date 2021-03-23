def group_fairness(metrics, maximum_acceptable_difference):
    satisfies_group_fairness = True
    metrics_amount = len(metrics)
    proportions = list()
    for i in range(metrics_amount):
        tp = metrics[i]["TP"]
        tn = metrics[i]["TN"]
        fp = metrics[i]["FP"]
        fn = metrics[i]["FN"]
        if tp+fp+tn+fn > 0:
            proportions.append((tp+fp)/(tp+fp+tn+fn))
        else:
            proportions.append(0)
    sorted_proportions = sorted(proportions)
    if sorted_proportions[metrics_amount-1] - sorted_proportions[0] > maximum_acceptable_difference:
        satisfies_group_fairness = False
    return satisfies_group_fairness, proportions
