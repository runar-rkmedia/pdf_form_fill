"""Part of smart pdf-form-filler (wip)"""
import pdffields.fields
import field_dicts


def logger(msg, msg_type='info'):
    """A logger function."""
    if msg_type == 'info':
        print ("{}: {}".format(msg_type, msg))

class FormField(object):
    """Wrapper for pdffields."""

    def __init__(self, pdf_path, fieldsDict):
        self.pdf_path = pdf_path
        self.fieldsDict = fieldsDict
        self.fields = self.set_fields_from_pdf()

    def set_fields_from_pdf(self):
        """Return all fields in the pdf."""
        return pdffields.fields.get_fields(self.pdf_path)

    def create_filled_pdf(self, filename, flatten=True):
        """Creates a pdf with all fields filled."""
        pdffields.fields.write_pdf(
            self.pdf_path, self.fields, filename, flatten)

    def set_field(self, fieldVariable, value):
        """Set a field in the pdf to a value."""
        thisDict = self.fieldsDict[fieldVariable]
        thisType = thisDict['type']
        if isinstance(value, thisType):
            self.fields[thisDict['field']] = value
            logger("Set field '{}' to '{}'".format(fieldVariable, value))
        else:
            raise ValueError("Expected a {} for fieldVariable = '{}' got value = '{}'".format(thisType, fieldVariable, value)) # noqa


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


nexans = FormField(
    '2012_Garantiskjema_V2_varmekabel_Nexans Norway.pdf', field_dicts.nexans)
varmecomfort = FormField(
    'Kontrollskjema_varme_2012.pdf', field_dicts.nexans)

print(varmecomfort.print_all_fields())
# print(nexans.print_all_fields())
# nexans.set_field('firma_navn', 'Kristiansand Elektro AS')
# nexans.set_field('anleggs_adresse', 'Rigetjonnveien 3')
# nexans.set_field('anleggs_adresse2', '4626 Kristiansand')
# nexans.set_field('Rom_navn', 'Bad')
# nexans.set_field('areal', 4.6)
# nexans.set_field('type_og_effekt', 'TXLP 500')
# nexans.set_field('meterEffekt', 17.0)
# nexans.set_field('nominell_motstand', 100)
# nexans.set_field('driftspenning', 230)
# nexans.create_filled_pdf('output.pdf')
# print(nexans_fields_dict['firma_navn']['text'])
