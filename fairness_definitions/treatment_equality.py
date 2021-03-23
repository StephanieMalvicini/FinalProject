def treatment_equality(metrics, maximum_acceptable_difference):
    satisfies_treatment_equality = True
    metrics_amount = len(metrics)
    errors = list()
    for i in range(metrics_amount):
        fp = metrics[i]["FP"]
        if fp == 0:
            errors.append(0)
        else:
            fn = metrics[i]["FN"]
            errors.append(fn/fp)
    sorted_errors = sorted(errors)
    if sorted_errors[metrics_amount-1] - sorted_errors[0] > maximum_acceptable_difference:
        satisfies_treatment_equality = False
    return satisfies_treatment_equality, errors
