#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part of smart pdf-form-filler (wip)"""
import pdffields.fields
from field_dicts import nexans


def logger(msg, msg_type='info'):
    """A logger function."""
    if msg_type == 'info':
        print ("{}: {}".format(msg_type, msg))


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
        if typeCheckBypass or isinstance(value, thisType):
            self.fields[thisDict['field']] = value
            logger("Set field '{}' to '{}'".format(fieldVariable, value))
        else:
            raise ValueError(
                "Expected a {} for fieldVariable = '{}' got value = '{}'".format(  # noqa
                    thisType, fieldVariable, value))

    def preprocess_format_dict(self, dictionary):
        """Fill specific fields in the formatting with info from dictionary."""
        for key, value in self.formatting.items():
            string_format = value[0]
            format_keys = value[1]
            expanded_values = []
            try:
                for f_key in format_keys:
                    expanded_values.append(dictionary[f_key])
                dictionary[key] = string_format.format(*expanded_values)
            except KeyError:
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
        '{} {}',
        ['type', 'effekt']]
}
nexans = FormField(
    '2012_Garantiskjema_V2_varmekabel_Nexans Norway.pdf',
    nexans.nexans,
    nexans_format)
# varmecomfort = FormField(
# 'Kontrollskjema_varme_2012.pdf', varmecomfort.varmecomfort)

# varmecomfort.fill_pdf_with_field_vars()
# varmecomfort.set_field('Inneanlegg_tradisjonell_stop_check', True)
# varmecomfort.set_field('Firma_adresse', 'Test')
# varmecomfort.set_field('anleggs_adresse', 'Test')
# varmecomfort.set_field('Kundenavn', 'Test')
# varmecomfort.set_field('Takrennefoler_antall', 2)
# varmecomfort.create_filled_pdf('output.pdf')

# print(varmecomfort.print_all_fields())
# print(nexans.print_all_fields())
standard_data = {
    'firma_navn': 'Kristiansand Elektro AS',
    'effekt': 800,
    'type': 'Kul',
}
nexans.set_fields_from_dict(standard_data)
