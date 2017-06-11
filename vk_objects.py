#!venv/bin/python
# Because of bug in Atom Beta or Atom Runnar, virtualenv is not activated.
# Please remove the above shebang, and use the one below in production.
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part of smart pdf-form-filler (wip)"""
import pdffields.fields
from field_dicts import nexans, oegleand
from field_dicts.helpers import NumberTypes
from subprocess import check_output
import subprocess
import sys


def setLoggerOptions(msg_type, enabled):
    """Will enable/disable a msg_type."""
    enabled_msg_types[msg_type] = enabled


enabled_msg_types = {'info': False,
                     'warning': True,
                     'fatal': True}


def logger(msg, msg_type='info'):
    """A logger function."""
    if enabled_msg_types.get(msg_type):
        print("{}: {}".format(msg_type, msg))


class FormField(object):
    """Wrapper for pdffields.

    args:
    pdf_path: path to pdf-form
    fields_dict: dictionary dumped by 'print_all_fields' and modified
    translator: a dict with a list containing a string  for formatting,
        and a lambda function to retrieve the data. Used to wrap generalized-
        data into this forms data.
    checkbox_value: for forms with checkboxes we need to know which values will
        check the box, and which will not. Should be a list of two values.
        To find this value, you can check some of the boxes in the form, save
        it and run 'pdftk file.pdf dump_data_fields_utf8' on it.
        e.g. ['true', 'false']

    """
    standard_data = {
        'type': 'TFXP',
        'driftspenning': '230',
        'sikringstørrelse': '16',
        'utløserstrøm_for_fordfeilvern': '30',
        'check-jordet_kabelskjerm': True,
        'check-toleder': True,
        'check-maks_temp_planlegging': True,
        'check-følertype-gulv': True,
        'check-installasjonsveiledning_fulgt': True
    }

    form_data_dict = {
        'Nexans': nexans,
        'Øglænd': oegleand
    }

    def __init__(self, manufacturor, standard_data=standard_data):
        form_data = self.form_data_dict.get(manufacturor)
        if not form_data:
            raise ValueError(
                "Could not find '{}' in dictionary when gathering form_data.")

        self.pdf_path = form_data.pdf_path
        self.fields_dict = form_data.fields_dict
        self.fields = self.set_fields_from_pdf()
        self.translator = form_data.translator
        self.checkbox_value = form_data.checkbox_value
        self.set_fields_from_dict(standard_data)

    def set_fields_from_pdf(self):
        """Return all fields in the pdf."""
        return pdffields.fields.get_fields(self.pdf_path)

    def create_filled_pdf(self, filename, flatten=False):
        """Creates a pdf with all fields filled."""
        pdffields.fields.write_pdf(
            self.pdf_path, self.fields, filename, flatten)

    def set_field(self, fieldVariable, value, typeCheckBypass=False):
        """Set a field in the pdf to a value."""
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
        logger("Set field '{}' to '{}'".format(fieldVariable, value))

    def preprocess_format_dict(self, dictionary):
        """Fill specific fields in the translator with info from dictionary."""
        for key, value in self.translator.items():
            string_format = value[0]
            format_keys = value[1]
            try:
                dictionary[key] = string_format.format(
                    *format_keys(dictionary))
            except (KeyError):
                pass

        return dictionary

    def set_fields_from_dict(self, dictionary):
        """Set multiple fields in pdf from a dictionary."""
        dictionary = self.preprocess_format_dict(dictionary)
        for key, value in dictionary.items():
            try:
                self.set_field(key, value)
            except KeyError:
                logger('Could not set field {}'.format(key))

    def print_all_fields(self):
        """Print all fields, to create the data-dictionary"""
        keyList = []
        for key in self.fields:
            fieldType = ''.join(c for c in key if not c.isnumeric())
            keyList.append("""'variable{0}':{{
   'text': 'TextInPDF',
   'field': '{0}',
   'type': '{1}'
            }}""".format(key, fieldType))
        return ',\n'.join(sorted(keyList))

    def fill_pdf_with_field_vars(self):
        """Fill all fields in the pdf with var-name from dict."""
        for key, value in self.fields_dict.items():
            self.set_field(key, key, True)

    def stamp_with_image(self, output_path, image, offsetx, offsety):
        """Will put image on top of this pdf"""
        # convert image to pdf
        call = [
            'java',
            '-jar',
            'pdfstamp/pdfstamp.jar',
            '-i',
            image,
            '-l',
            '10,10',
            output_path]
        print(call)
        check_output(call).decode('utf8')

if __name__ == '__main__':
    pass
