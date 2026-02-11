"""Utilities: validation and constants."""


def validate_positive_number(value):
    """Validate that input is a positive number."""
    try:
        num = float(value)
        if num < 0:
            raise ValueError("Values must be non-negative")
        return num
    except ValueError as e:
        if "Values must be non-negative" in str(e):
            raise
        raise ValueError("Invalid input: please enter a valid number")


# Standard concentration unit across app
STANDARD_CONC_UNIT = "ng/µL"
