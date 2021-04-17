def conditional_use_accuracy_equality(metrics, maximum_acceptable_difference):
    satisfies_conditional_use_accuracy_equality = True
    metrics_amount = len(metrics)
    ppv = list()
    npv = list()
    for i in range(metrics_amount):
        tp = metrics[i]["TP"]
        tn = metrics[i]["TN"]
        fp = metrics[i]["FP"]
        fn = metrics[i]["FN"]
        if tp+fp > 0:
            ppv.append(tp/(tp+fp))
        else:
            ppv.append(0)
        if tn+fn > 0:
            npv.append(tn/(tn+fn))
        else:
            npv.append(0)
    sorted_ppv = sorted(ppv)
    sorted_npv = sorted(npv)
    if sorted_ppv[metrics_amount-1] - sorted_ppv[0] > maximum_acceptable_difference:
        satisfies_conditional_use_accuracy_equality = False
    elif sorted_npv[metrics_amount-1] - sorted_npv[0] > maximum_acceptable_difference:
        satisfies_conditional_use_accuracy_equality = False
    return satisfies_conditional_use_accuracy_equality, ppv, npv
