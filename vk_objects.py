#!venv/bin/python
# Because of bug in Atom Beta or Atom Runnar, virtualenv is not activated.
# Please remove the above shebang, and use the one below in production.
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part of smart pdf-form-filler (wip)"""
import pdffields.fields
from field_dicts import nexans
from field_dicts.field_dicts import NumberTypes


def logger(msg, msg_type='info'):
    """A logger function."""
    if msg_type == 'info':
        print("{}: {}".format(msg_type, msg))


class FormField(object):
    """Wrapper for pdffields."""

    def __init__(self, pdf_path, fields_dict, formatting):
        self.pdf_path = pdf_path
        self.fields_dict = fields_dict
        self.fields = self.set_fields_from_pdf()
        self.formatting = formatting

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
                value = 'Yes'
            else:
                value = 'No'
        self.fields[thisDict['field']] = value
        logger("Set field '{}' to '{}'".format(fieldVariable, value))

    def preprocess_format_dict(self, dictionary):
        """Fill specific fields in the formatting with info from dictionary."""
        for key, value in self.formatting.items():
            print(key)
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
            print(key, value['field'], value['text'])
            self.set_field(key, key, True)


nexans_format = {
    'type_og_effekt': [
        '{} {:.0f}',
        lambda x: (x['type'], float(x['effekt']))
    ],
    'flateeffekt': [
        '{:.2f}',
        lambda x: (float(x['effekt']) / float(x['oppvarmet_areal']),)
    ]
}
nexans_format = {
    'type_og_effekt': [
        '{} {:.0f}',
        lambda x: (x['type'], float(x['effekt']))
    ],
    'flateeffekt': [
        '{:.2f}',
        lambda x: (float(x['effekt']) / float(x['oppvarmet_areal']),)
    ]
}
nexans = FormField(
    '2012_Garantiskjema_V2_varmekabel_Nexans Norway.pdf',
    nexans.nexans,
    nexans_format)
standard_data = {
    'firma_navn': 'Kristiansand Elektro AS',
    'type': 'TFXP',
    'driftspenning': '230',
    'sikringstørrelse': '16',
    'utløserstrøm_for_fordfeilvern': '30',
    'check-jordet_kabelskjerm': True,
    'check-toleder': True
}
# nexans.set_fields_from_d§ict(standard_data)

if __name__ == '__main__':
    standard_data['areal'] = '9'
    standard_data['effekt'] = '700'
    standard_data['type'] = 'TFXP'
    standard_data['oppvarmet_areal'] = '5.48'
    nexans.set_fields_from_dict(standard_data)
    # nexans.fill_pdf_with_field_vars()
    nexans.create_filled_pdf('output.pdf')
