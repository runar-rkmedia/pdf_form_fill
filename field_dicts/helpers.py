"""part of smart pdf filler."""
from time import gmtime, strftime
import string
import random
NumberTypes = (int, float, complex)


def currentDate():
    """Get formated current date."""
    return strftime("%d.%m.%Y", gmtime())


def commafloat(string_as_number):
    """Return a float from string with comma as decimal-seperator."""
    return float(string_as_number.replace(',', '.'))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Return random string with digits."""
    return ''.join(random.choice(chars) for _ in range(size))


def group_number(n, grouping=3, seperator=' '):
    """Returns a pretty, grouped number."""
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
