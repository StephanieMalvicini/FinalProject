def validate_test_size(value):
    if value.isdigit() and (int(value) in range(1, 101)):
        return True
    else:
        return False
