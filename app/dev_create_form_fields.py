"""Create the fields-dictionary for a new pdf-form."""

from field_dicts.pdf_form import PdfForm
import pdffields


class DevPDF(PdfForm):

    def __init__(self, pdf_path):
        """Description."""
        super().__init__([], pdf_path, [''], ['', ''])
        self.fields = self.set_fields_from_pdf()

    def set_fields_from_pdf(self):
        """Return all fields in the pdf."""
        return pdffields.fields.get_fields(self.pdf_path)

    def fill_pdf_with_field_vars(self):
        """Fill all fields in the pdf with var-name from dict."""
        for key, value in self.fields_dict.items():
            self.set_field(key, key, True)

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


devform = DevPDF('static/forms/Samsvarserklæring_01_17_skjemautfylling.pdf')
print(devform.print_all_fields())
