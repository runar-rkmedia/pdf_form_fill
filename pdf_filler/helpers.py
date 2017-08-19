"""part of smart pdf filler."""
from time import gmtime, strftime
import string
import random
NumberTypes = (int, float, complex)


def currentDate(date_format="%d.%m.%Y"):
    """Get formated current date."""
    return strftime(date_format, gmtime())


def commafloat(string_as_number):
    """Return a float from string with comma as decimal-seperator."""
    if isinstance(string_as_number, float):
        return string_as_number
    elif isinstance(string_as_number, str):
        return float(string_as_number.replace(',', '.'))
    else:
        raise ValueError('{} is not a string, or a float, but {}'.format(
            string_as_number, type(string_as_number)
        ))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Return random string with digits."""
    return ''.join(random.choice(chars) for _ in range(size))


def delete_empty_value(dictionary):
    """Remove all keys from a dictionary where values are empty."""
    return {k: v for k, v in dictionary.items() if v != None and v != ''}  # noqa


def group_number(n, grouping=3, seperator=' '):
    """Returns a pretty, grouped number."""
    try:
        # 10x performance
        if grouping == 3:
            s = format(n, ',')
            if seperator == ',':
                return s
            return s.replace(',', seperator)
        # Slow, general grouping
        else:
            r = []
            for i, c in enumerate(reversed(str(n))):
                if i and (not (i % grouping)):
                    r.insert(0, seperator)
                r.insert(0, c)
            return ''.join(r)
    except ValueError:
        return n


def month_name(month_number, short=False):
    """Return the name of the month."""
    months = [
        'januar',
        'februar',
        'mars',
        'april',
        'mai',
        'juni',
        'juli',
        'august',
        'september',
        'oktober',
        'november',
        'desember',
    ]
    month_name = months[month_number - 1]
    if short:
        return month_name[:3]
    return month_name


class DictionaryHelper(object):

    def __init__(self, dictionary):
        """Some helper functions for dictionaries."""
        self.dictionary = dictionary

    def g(self, key, default=''):
        """
        Alias for self.dictionary.get, with string-casting

        Also handles returned values that themselves are empty.

        Example:
        a = {'myKey': None}

        Will still return default-value, not None.

        """
        value = self.dictionary.get(key, default)
        return value or default

    def s(self, key, default=''):
        """shortcut for this.g, but with stringcasting."""
        return str(self.g(key, default))

    def s_if(self, key, pre='', sub='', default=''):
        """Output value if key, with pre and/or subfix."""
        string = self.s(key, default)
        if len(string) > 0:
            return '{}{}{}'.format(pre, string, sub)
        return default
