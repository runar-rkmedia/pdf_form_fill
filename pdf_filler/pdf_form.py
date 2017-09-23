import os

import pdffields.fields

from .helpers import NumberTypes, delete_empty_value
import collections
from decimal import Decimal


def replace_None(d, default=''):
    """
    Replace None in a nested dictionary.

    0-values are preserved, only strict None is replaced.

    Code is modified from Martijn Pieters at
    https://stackoverflow.com/a/27974027
    """
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [
            v if v is not None else default
            for v in (replace_None(v)
                      for v in d)
        ]
    return {k:
            v if v is not None else default
            for k, v in ((k, replace_None(v))
                         for k, v in d.items())}


class PdfForm(object):

    def __init__(self,
                 dictionary,
                 fill_pdf_filename,
                 fields_dict,
                 checkbox_value):
        self.dictionary = replace_None(dictionary)
        self.fields = {}
        self.fields_dict = fields_dict
        self.fill_pdf_path = os.path.join('static', 'forms', fill_pdf_filename)
        self.checkbox_value = checkbox_value

    def dict_update(self, dictionary):
        self.dictionary.update(dictionary)

    def translate(self):
        raise NotImplementedError(
            "{} missing translate-method".format(type(self)))

    def translate_common(self):
        def parse_float(d, u):
            """Parse all floats in a nested dictionary."""
            for k, v in u.items():
                if isinstance(v, collections.Mapping):
                    r = parse_float(d.get(k, {}), v)
                    d[k] = r
                elif isinstance(v, bool):
                    d[k] = self.checkbox_value[0] if v else self.checkbox_value[1]
                elif isinstance(v, (float, Decimal, str)):
                    d[k] = v
                    try:
                        d[k] = ('%.2f' % float(v)).rstrip('0').rstrip('.')
                    except (TypeError, ValueError):
                        pass
                else:
                    d[k] = u[k]
            return d
        self.dictionary = parse_float({}, self.dictionary)

    def set_fields_from_dict(self):
        """Set multiple fields in pdf from a dictionary."""
        for key, value in self.dictionary.items():
            try:
                self.set_field(key, value)
            except KeyError:
                pass

    def set_field(self, fieldVariable, value):
        """ Set a field in the pdf to a value. """
        thisDict = self.fields_dict[fieldVariable]
        self.fields[thisDict['field']] = value

    def create_filled_pdf(self, filename, flatten=False):
        """Creates a pdf with all fields filled."""
        self.translate()
        self.translate_common()
        self.set_fields_from_dict()
        pdffields.fields.write_pdf(
            self.fill_pdf_path, self.fields, filename, flatten)
        return delete_empty_value(self.fields)
