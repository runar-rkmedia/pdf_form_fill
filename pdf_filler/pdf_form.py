import pdffields.fields
from .helpers import delete_empty_value, NumberTypes
import os


class PdfForm(object):

    def __init__(self,
                 dictionary,
                 fill_pdf_filename,
                 fields_dict,
                 checkbox_value):
        self.dictionary = dictionary
        self.fields = {}
        self.fields_dict = fields_dict
        self.fill_pdf_path = os.path.join('static', 'forms', fill_pdf_filename)
        self.checkbox_value = checkbox_value

    def dict_update(self, dictionary):
        self.dictionary.update(dictionary)

    def translate(self):
        raise NotImplementedError(
            "{} missing translate-method".format(type(self)))

    def set_fields_from_dict(self):
        """Set multiple fields in pdf from a dictionary."""
        for key, value in self.dictionary.items():
            try:
                self.set_field(key, value)
            except KeyError:
                pass

    def set_field(self, fieldVariable, value, typeCheckBypass=False):
        """
        Set a field in the pdf to a value.

        Will also typecast, and thereby also set the bool-values correctly
        to whatever checkbox_value is set to. (Like, 'yes', 'no').

        The reason for this is that some pdf's uses text instead of an actual
        bool-value to set the checkbox.
        """
        thisDict = self.fields_dict[fieldVariable]
        thisType = thisDict['type']
        # Cast the value to the needed type.
        if thisType == NumberTypes and not isinstance(value, thisType):
            for t in NumberTypes:
                try:
                    value = t(value)
                    break
                except ValueError:
                    pass
        elif thisType == bool:
            if value:
                value = self.checkbox_value[0]
            else:
                value = self.checkbox_value[1]
        self.fields[thisDict['field']] = value

    def create_filled_pdf(self, filename, flatten=False):
        """Creates a pdf with all fields filled."""
        self.translate()
        self.set_fields_from_dict()
        pdffields.fields.write_pdf(
            self.fill_pdf_path, self.fields, filename, flatten)
        return delete_empty_value(self.fields)
