def false_positive_error_rate_balance(metrics, maximum_acceptable_difference):
    satisfies_false_positive_error_rate_balance = True
    metrics_amount = len(metrics)
    fpr = list()
    for i in range(metrics_amount):
        tn = metrics[i]["TN"]
        fp = metrics[i]["FP"]
        if fp+tn > 0:
            fpr.append(fp/fp+tn)
        else:
            fpr.append(0)
    sorted_fpr = sorted(fpr)
    if sorted_fpr[metrics_amount - 1] - sorted_fpr[0] > maximum_acceptable_difference:
        satisfies_false_positive_error_rate_balance = False
    return satisfies_false_positive_error_rate_balance, sorted_fpr
