def validate_int_range(str_value, first_value, last_value):
    if str_value.isdigit() and (int(str_value) in range(first_value, last_value + 1)):
        return True
    else:
        return False


def validate_float(str_value, decimals):
    is_valid = False
    try:
        value = float(str_value)
        if (value >= 0) and (value <= 1) and (len(str_value.rsplit('.')[-1]) <= decimals):
            is_valid = True
    except ValueError:
        pass
    return is_valid


def validate_test_size(str_value):
    if len(str_value) == 0:
        return True
    return validate_int_range(str_value, 1, 100)


def validate_maximum_acceptable_difference(str_value):
    return validate_float(str_value, 2)


def validate_error(str_value):
    return validate_int_range(str_value, 0, 100)


def validate_minimum_samples_amount(str_value):
    if len(str_value) == 0:
        return True
    return str_value.isdigit() and int(str_value) > 0


def validate_decimals(str_value):
    return validate_int_range(str_value, 0, 5)


def validate_attribute_value_numeric(str_value):
    if len(str_value) == 0:
        return True
    try:
        int(str_value)
        return True
    except ValueError:
        pass
    try:
        float(str_value)
        return True
    except ValueError:
        pass
    return False
