def overall_accuracy_equality(metrics, maximum_acceptable_difference):
    satisfies_overall_accuracy_equality = True
    metrics_amount = len(metrics)
    precisions = list()
    for i in range(metrics_amount):
        tp = metrics[i]["TP"]
        tn = metrics[i]["TN"]
        fp = metrics[i]["FP"]
        fn = metrics[i]["FN"]
        if tp+fp+tn+fn > 0:
            precisions.append((tp+tn)/(tp+fp+tn+fn))
        else:
            precisions.append(0)
    sorted_precisions = sorted(precisions)
    if sorted_precisions[metrics_amount-1] - sorted_precisions[0] > maximum_acceptable_difference:
        satisfies_overall_accuracy_equality = False
    return satisfies_overall_accuracy_equality, precisions
