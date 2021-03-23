def false_negative_error_rate_balance(metrics, maximum_acceptable_difference):
    satisfies_false_negative_error_rate_balance = True
    metrics_amount = len(metrics)
    fnr = list()
    for i in range(metrics_amount):
        fn = metrics[i]["FN"]
        tp = metrics[i]["TP"]
        if tp+fn > 0:
            fnr.append(fn/tp+fn)
        else:
            fnr.append(0)
    sorted_fnr = sorted(fnr)
    if sorted_fnr[metrics_amount - 1] - sorted_fnr[0] > maximum_acceptable_difference:
        satisfies_false_negative_error_rate_balance = False
    return satisfies_false_negative_error_rate_balance, sorted_fnr
