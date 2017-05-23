"""part of smart pdf filler."""
from time import gmtime, strftime
NumberTypes = (int, float, complex)


def currentDate():
    """Get formated current date."""
    return strftime("%d.%m.%Y", gmtime())


def commafloat(string_as_number):
    """Return a float from string with comma as decimal-seperator."""
    return float(string_as_number.replace(',', '.'))
