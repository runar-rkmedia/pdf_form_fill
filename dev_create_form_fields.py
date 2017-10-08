"""Create the fields-dictionary for a new pdf-form."""

from pdf_filler.pdf_form import PdfForm
import pdffields
from pdf_filler.thermofloor_cable import ThermoFloorCable


class DevPDF(PdfForm):

    def __init__(self, fill_pdf_filename):
        """Description."""
        super().__init__({},
                         fill_pdf_filename,
                         {},
                         ['',''])
        self.fields = self.set_fields_from_pdf()

    def set_fields_from_pdf(self):
        """Return all fields in the pdf."""
        return pdffields.fields.get_fields(self.fill_pdf_path)

    def fill_pdf_with_field_vars(self):
        """Fill all fields in the pdf with var-name from dict."""
        for key, value in self.fields.items():
            self.fields[key] = key

    def translate(self):
        pass

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


devform = DevPDF('Dokumentasjonssider_varmekabel_Ver2016-A.pdf')
devform.fill_pdf_with_field_vars()
devform.create_filled_pdf('test.pdf')
print(devform.print_all_fields())
