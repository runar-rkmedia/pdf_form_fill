# -*- coding: utf-8 -*-
"""Data for øglænd-dictionary."""
from .helpers import NumberTypes, month_name, group_number, DictionaryHelper
from .stamp import StampablePdfForm, signatere_location_size


class Oegleand(StampablePdfForm):

    def __init__(self, dictionary):
        super().__init__(
            dictionary=dictionary,
            fill_pdf_filename=self.FILL_PDF_FILENAME,
            fields_dict=self.FIELDS_DICT,
            checkbox_value=self.CHECKBOX_VALUE,
            signature_location_sizes=[
                signatere_location_size(x=259, y=59, w=228, h=33)
            ])

    def translate(self):

        d = DictionaryHelper(self.dictionary)
        self.dict_update({
            'anleggs_adresse':
                d.s('customer.address.address1') + ' ' +
                d.s('customer.address.address2') + '\n' +
                d.s('customer.address.post_code') + ' ' +
                d.s('customer.address.post_area'),
            'company.orgnumber': group_number(d.g('company.orgnumber')),
            'product.resistance_min': '{0:.1f}'.format(
                d.g('product.resistance_min')
                )
        })

        date = d.g('date')
        if date:
            self.dict_update({
                'dato-År': date.year,
                'dato-måned': month_name(date.month, short=True),
                'dato-dag': date.day
            })

    FILL_PDF_FILENAME = 'Samsvarserklæring_01_17_skjemautfylling.pdf'
    CHECKBOX_VALUE = ['Ja', 'Nei']

    FIELDS_DICT = {
        'dato-År': {
            'text': 'TextInPDF',
            'field': 'År',
            'type': str
        },
        'company.address.address1': {
            'text': 'TextInPDF',
            'field': 'Adresse Installatør',
            'type': str
        },
        'anleggs_adresse': {
            'text': 'TextInPDF',
            'field': 'Adresse installasjonssted',
            'type': str
        },
        'innendoers_innstallasjon_annet': {
            'text': 'TextInPDF',
            'field': 'Annet',
            'type': bool
        },
        'room.heated_area': {
            'text': 'TextInPDF',
            'field': 'Areal m2',
            'type': NumberTypes
        },
        'Asf': {
            'text': 'TextInPDF',
            'field': 'Asf',
            'type': bool
        },
        'Bren': {
            'text': 'TextInPDF',
            'field': 'Bren',
            'type': bool
        },
        'dato-dag': {
            'text': 'TextInPDF',
            'field': 'Dag',
            'type': str
        },
        'check-Dokumentasjon-overlevert': {
            'text': 'TextInPDF',
            'field': 'Doku',
            'type': bool
        },
        'product.effect': {
            'text': 'TextInPDF',
            'field': 'Effekt W',
            'type': str
        },
        'check-Eier-informert': {
            'text': 'TextInPDF',
            'field': 'Eier',
            'type': bool
        },
        'room.name': {
            'text': 'TextInPDF',
            'field': 'Eks bad, gang',
            'type': str
        },
        'Fart': {
            'text': 'TextInPDF',
            'field': 'Fart',
            'type': bool
        },
        'company.name': {
            'text': 'TextInPDF',
            'field': 'Firmanavn',
            'type': str
        },
        'Frost': {
            'text': 'TextInPDF',
            'field': 'Frost',
            'type': bool
        },
        'frostsikringstype': {
            'text': 'TextInPDF',
            'field': 'Frostsikringsstyring type',
            'type': str
        },
        'product.product_type.name': {
            'text': 'TextInPDF',
            'field': 'Hovedgruppe',
            'type': str
        },
        'Infor': {
            'text': 'TextInPDF',
            'field': 'Infor',
            'type': bool
        },
        'Inn Be': {
            'text': 'TextInPDF',
            'field': 'Inn Be',
            'type': bool
        },
        'mohm_a': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ inst',
            'type': str
        },
        'mohm_b': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ støp',
            'type': str
        },
        'mohm_c': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ tilk',
            'type': str
        },
        'check-jordfeilbryter-30mA': {
            'text': 'TextInPDF',
            'field': 'Jord',
            'type': bool
        },
        'company.contact_person': {
            'text': 'TextInPDF',
            'field': 'Kontaktperson',
            'type': 'Kontaktperson'
        },
        'check-innendørs-lamiflex': {
            'text': 'TextInPDF',
            'field': 'Lam',
            'type': bool
        },
        'check-innendørs-lavtbygggende-gult': {
            'text': 'TextInPDF',
            'field': 'Lavt',
            'type': bool
        },
        'dato-måned': {
            'text': 'TextInPDF',
            'field': 'Mnd',
            'type': str
        },
        'check-beskyttelses-tiltak-monteringsanvisning-fulgt': {
            'text': 'TextInPDF',
            'field': 'Mont',
            'type': bool
        },
        'company.orgnumber': {
            'text': 'TextInPDF',
            'field': 'Organisasjonsnr',
            'type': str
        },
        'Overdekning_mm': {
            'text': 'TextInPDF',
            'field': 'Overdekning',
            'type': NumberTypes
        },
        'check-utendørs-frostsikring-rør–innendig': {
            'text': 'TextInPDF',
            'field': 'Rør in',
            'type': bool
        },
        'check-utendørs-frostsikring-rør–utvendig': {
            'text': 'TextInPDF',
            'field': 'Rør ut',
            'type': bool
        },
        'ohm_a': {
            'text': 'TextInPDF',
            'field': 'Resistans Ω inst',
            'type': NumberTypes
        },
        'ohm_b': {
            'text': 'TextInPDF',
            'field': 'Resistans Ω støp',
            'type': NumberTypes
        },
        'ohm_c': {
            'text': 'TextInPDF',
            'field': 'Resistans Ω tilk',
            'type': NumberTypes
        },
        'product.resistance_max': {
            'text': 'TextInPDF',
            'field': 'Resistans max Ω',
            'type': NumberTypes
        },
        'product.resistance_min': {
            'text': 'TextInPDF',
            'field': 'Resistans min Ω',
            'type': NumberTypes
        },
        'styring-smeltestyringstype': {
            'text': 'TextInPDF',
            'field': 'Snøsmeltestyringstype',
            'type': str
        },
        'product.voltage': {
            'text': 'TextInPDF',
            'field': 'Spenning V',
            'type': NumberTypes
        },
        'innendørs_annet_spesifiser': {
            'text': 'TextInPDF',

            'field': 'Spesifiser',
            'type': str
        },
        'check-utendørs_belegningsstein-heller': {
            'text': 'TextInPDF',
            'field': 'Stei',
            'type': bool
        },
        'check-beskyttelses-tiltak-bruk-av-styring': {
            'text': 'TextInPDF',
            'field': 'Styr',
            'type': bool
        },
        'company.phone': {
            'text': 'TextInPDF',
            'field': 'Telefon',
            'type': str
        },
        'product.name': {
            'text': 'TextInPDF',
            'field': 'Type kabel/matte',
            'type': str
        },
        'check-innendørs-varmematte_ubrennbart_underlag': {
            'text': 'TextInPDF',
            'field': 'Ubre',
            'type': bool
        },
        'installatør_underskrift': {
            'text': 'TextInPDF',
            'field': 'Underskrift',
            'type': str
        },
        'check-utendørs-betong': {
            'text': 'TextInPDF',
            'field': 'Ut Bet',
            'type': bool
        },
        'watt_per_square_meter': {
            'text': 'TextInPDF',
            'field': 'W/m2',
            'type': NumberTypes
        },
        'check-følertype-annet': {
            'text': 'TextInPDF',
            'field': 'annet',
            'type': bool
        },
        'check-følertype-begrensningsføler': {
            'text': 'TextInPDF',
            'field': 'begr',
            'type': bool
        },
        'cc': {
            'text': 'TextInPDF',
            'field': 'c/c',
            'type': NumberTypes
        },
        'check-følertype-gulv': {
            'text': 'TextInPDF',
            'field': 'gulv',
            'type': bool
        },
        'check-følertype-rom': {
            'text': 'TextInPDF',
            'field': 'rom',
            'type': bool
        }
    }
