def is_number(string):
    if string.isnumeric():
        return True
    try:
        float(string)
        return True
    except ValueError:
        return False