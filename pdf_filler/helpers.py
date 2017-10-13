"""part of smart pdf filler."""
import random
import string
from time import gmtime, strftime

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

class NumberFormatter(object):
    """Formats numbers in different formats."""

    @staticmethod
    def group_number_format(n, grouping_list, sep=' ', default=''):
        """
        General grouping of numbers.

        grouping_list should be a list of numbers.

        example: [3,2,3] will group by 3, then 2, then 3.

        """
        if not n:
            return default
        n = str(n)
        group = []
        i = 0
        for c in grouping_list:
            group.append(n[i:i + c])
            i += c
        return sep.join(group)

    @classmethod
    def phone(cls, n):
        """Return a formatted phone-numer."""
        return cls.group_number_format(n, [2, 2, 2, 2])

    @classmethod
    def mobile(cls, n):
        """Return a formatted mobile-number."""
        return cls.group_number_format(n, [3, 2, 3])


    @classmethod
    def org(cls, n):
        """Return a formatted organizaion-number."""
        return cls.group_number_format(n, [3, 3, 3])

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
    m_name = months[month_number - 1]
    if short:
        return m_name[:3]
    return m_name


def date_format(date, format_='{d}. {M} {y}'):
    """
    Custom date-format.

    args:
    'date': the date to format.
    'format_': the format to use. Should be a string. Can have these values:

    d: the day of the month.
    m: the month, numerical.
    M: the month, string, short,
    MM: the month, string, long.
    y: the year.

    Example format: '{d}. {M} {y}'

    """
    return format_.format(**{
        'y': date.year,
        'M': month_name(date.month, short=True),
        'MM': month_name(date.month, short=False),
        'm': date.month,
        'd': date.day
    })


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
        s = self.s(key, default)
        if len(s) > 0:
            return '{}{}{}'.format(pre, s, sub)
        return default

    def s_bool(self, key):
        """Output the boolean if field exists"""
        return len(self.s(key)) > 0


class OhmsLaw(object):
    """Various functions for calculating electricity."""

    def __init__(self, voltage=0, power=0, resistance=0, current=0):
        self._P = float(power)
        self._U = float(voltage)
        self._I = float(current)
        self._R = float(0)
        self.resistance = resistance

    @property
    def voltage(self):
        if self._R and self._I:
            return self._I * self._R
        if self._P and self._I:
            return self._P / self._I
        if self._P and self._R:
            return (self._P * self._R)**0.5
        return self._U

    @property
    def current(self):
        if self._R and self._U:
            return self._U / self._R
        if self._P and self._U:
            return self._P / self._U
        if self._P and self._R:
            return (self._P / self._R)**.5
        return self._I

    @property
    def resistance(self):
        if self._I and self._U:
            return self._U / self._I
        if self._P and self._U:
            return self._U**2 / self._P
        if self._P and self._I:
            return self._P / self._I**2
        return self._R

    @property
    def power(self):
        if self._I and self._U:
            return self._U * self._I
        if self._R and self._U:
            return self._U**2 / self._R
        if self._R and self._I:
            return self._I**2 * self._R
        return self._P

    @voltage.setter
    def voltage(self, value):
        self._U = float(value)

    @power.setter
    def power(self, value):
        self._P = float(value)

    @current.setter
    def current(self, value):
        self._I = float(value)

    @resistance.setter
    def resistance(self, values):
        """
        Set resistance.

        If value is a list of floats, it will set the resistance to total
        resistance by treating the list of floats as a list of resistors in
        parallell.

        For serial-calculations, just sum them together.
        """
        if isinstance(values, list):
            values = self.total_resistance_paralell(values)
        self._R = float(values)

    @staticmethod
    def total_resistance_paralell(list_of_values):
        """Return total resistance from a list of resistor-values."""
        R = 0
        for value in list_of_values:
            if value > 0:
                R += 1.0/value
        return 1/R

    def __repr__(self):
        return '{:4.2f} V, {:4.2f} W, {:4.2f} Ω, {:4.2f} A'.format(
            self.voltage, self.power, self.resistance, self.current)
