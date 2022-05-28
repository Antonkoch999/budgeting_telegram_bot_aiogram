"""Module contains help functions."""


def check_is_digit(number):
    """Check the number if the amount that we enter."""
    try:
        amount = round(float(number), 2)
    except ValueError:
        amount = 0

    return amount


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
