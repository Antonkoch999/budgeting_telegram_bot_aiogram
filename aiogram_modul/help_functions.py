"""Module contains help functions."""


def check_is_digit(number):
    """Check the number if the amount that we enter."""
    try:
        amount = round(float(number), 2)
    except ValueError:
        amount = 0

    return amount
