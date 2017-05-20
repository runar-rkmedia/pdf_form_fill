"""Helper-functions."""


def commafloat(string_as_number):
    """Return a float from string with comma as decimal-seperator."""
    return float(string_as_number.replace(',', '.'))
