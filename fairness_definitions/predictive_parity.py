def predictive_parity(metrics, maximum_acceptable_difference):
    satisfies_predictive_parity = True
    metrics_amount = len(metrics)
    ppv = list()
    for i in range(metrics_amount):
        tp = metrics[i]["TP"]
        fp = metrics[i]["FP"]
        if tp+fp > 0:
            ppv.append(tp/(tp+fp))
        else:
            ppv.append(0)
    sorted_ppv = sorted(ppv)
    if sorted_ppv[metrics_amount-1] - sorted_ppv[0] > maximum_acceptable_difference:
        satisfies_predictive_parity = False
    return satisfies_predictive_parity, ppv
