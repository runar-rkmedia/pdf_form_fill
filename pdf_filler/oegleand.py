# -*- coding: utf-8 -*-
"""Data for øglænd-dictionary."""
from .helpers import DictionaryHelper, NumberTypes, group_number, month_name
from .stamp import StampablePdfForm, signatere_location_size

TRUE = 'Ja'
FALSE = 'Nei'


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
            'control_system_other_check': d.s_bool('control_system_other'),
            'anleggs_adresse':
                d.s('customer.address.address1') + ' ' +
                d.s('customer.address.address2') + '\n' +
                d.s('customer.address.post_code') + ' ' +
                d.s('customer.address.post_area'),
            'product.resistance_min': '{0:.1f}'.format(
                d.g('product.resistance_min')
            )
        })
        self.dictionary['control_system_other_check'] = TRUE
        date = self.dictionary.get('last_date')

        if (
            d.s_bool('control_system_room_sensor') or
            d.s_bool('control_system_floor_sensor') or
            d.s_bool('control_system_limit_sensor') or
            d.s_bool('control_system_other')
            ):
            self.dictionary['control_system_check_any'] = TRUE
        self.dict_update({
            'company.phone': d.g('company.contact.phone_f', d.g('company.contact.mobile_f')),
        })
        self.dict_update({
            'company.installer_name__': d.g('company.name'),
        })
        self.dictionary['inside_specs.not_fireproof'] = FALSE if self.dictionary.get('inside_specs.fireproof') else TRUE
        self.dictionary['inside_specs.other_check'] = TRUE if self.dictionary.get('inside_specs.other') else FALSE
        if  1 <= self.dictionary.get('ground_fault_protection', -1) <= 30:
            self.dictionary['check-jordfeilbryter-30mA'] = TRUE

        if date:
            self.dict_update({
                'dato-År': date.year,
                'dato-måned': month_name(date.month, short=True),
                'dato-dag': date.day
            })

    FILL_PDF_FILENAME = 'Samsvarserklæring_01_17_skjemautfylling.pdf'
    CHECKBOX_VALUE = [TRUE, FALSE]

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
        'inside_specs.other_check': {
            'text': 'TextInPDF',
            'field': 'Annet',
            'type': bool
        },
        'room.heated_area': {
            'text': 'TextInPDF',
            'field': 'Areal m2',
            'type': NumberTypes
        },
        'outside_specs.asphalt': {
            'text': 'TextInPDF',
            'field': 'Asf',
            'type': bool
        },
        'inside_specs.fireproof': {
            'text': 'TextInPDF',
            'field': 'Bren',
            'type': bool
        },
        'dato-dag': {
            'text': 'TextInPDF',
            'field': 'Dag',
            'type': str
        },
        'handed_to_owner': {
            'text': 'TextInPDF',
            'field': 'Doku',
            'type': bool
        },
        'product.effect': {
            'text': 'TextInPDF',
            'field': 'Effekt W',
            'type': str
        },
        'owner_informed': {
            'text': 'TextInPDF',
            'field': 'Eier',
            'type': bool
        },
        'room.name': {
            'text': 'TextInPDF',
            'field': 'Eks bad, gang',
            'type': str
        },
        'outside_specs.vessel': {
            'text': 'TextInPDF',
            'field': 'Fart',
            'type': bool
        },
        'company.installer_name__': {
            'text': 'TextInPDF',
            'field': 'Firmanavn',
            'type': str
        },
        'outside_specs.frost_protection': {
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
        'max_temp_planning': { # hva er dette?
            'text': 'TextInPDF',
            'field': 'Infor',
            'type': bool
        },
        'inside_specs.concrete': {
            'text': 'TextInPDF',
            'field': 'Inn Be',
            'type': bool
        },
        'install.mohm': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ inst',
            'type': str
        },
        'pour.mohm': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ støp',
            'type': str
        },
        'connect.mohm': {
            'text': 'TextInPDF',
            'field': 'Isolasjonstest MΩ tilk',
            'type': str
        },
        'check-jordfeilbryter-30mA': {
            'text': 'TextInPDF',
            'field': 'Jord',
            'type': bool
        },
        'company.contact_name': {
            'text': 'TextInPDF',
            'field': 'Kontaktperson',
            'type': 'Kontaktperson'
        },
        'inside_specs.LamiFlex': {
            'text': 'TextInPDF',
            'field': 'Lam',
            'type': bool
        },
        'inside_specs.low_profile': {
            'text': 'TextInPDF',
            'field': 'Lavt',
            'type': bool
        },
        'dato-måned': {
            'text': 'TextInPDF',
            'field': 'Mnd',
            'type': str
        },
        'max_temp_installation': {
            'text': 'TextInPDF',
            'field': 'Mont',
            'type': bool
        },
        'company.orgnumber_f': {
            'text': 'TextInPDF',
            'field': 'Organisasjonsnr',
            'type': str
        },
        'installation_depth': {
            'text': 'TextInPDF',
            'field': 'Overdekning',
            'type': NumberTypes
        },
        'inside_specs.frost_protection_pipe': {
            'text': 'TextInPDF',
            'field': 'Rør in',
            'type': bool
        },
        'outside_specs.frost_protection_pipe': {
            'text': 'TextInPDF',
            'field': 'Rør ut',
            'type': bool
        },
        'install.ohm': {
            'text': 'TextInPDF',
            'field': 'Resistans Ω inst',
            'type': NumberTypes
        },
        'pour.ohm': {
            'text': 'TextInPDF',
            'field': 'Resistans Ω støp',
            'type': NumberTypes
        },
        'connect.ohm': {
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
        'inside_specs.other': {
            'text': 'TextInPDF',

            'field': 'Spesifiser',
            'type': str
        },
        'outside_specs.paving_stones': {
            'text': 'TextInPDF',
            'field': 'Stei',
            'type': bool
        },
        'control_system_other_check': { # Why U no work?
            'text': 'TextInPDF',
            'field': 'Styr',
            'type': bool
        },
        'company.contact_phone_f': {
            'text': 'TextInPDF',
            'field': 'Telefon',
            'type': str
        },
        'product.name': {
            'text': 'TextInPDF',
            'field': 'Type kabel/matte',
            'type': str
        },
        'inside_specs.not_fireproof': {
            'text': 'TextInPDF',
            'field': 'Ubre',
            'type': bool
        },
        'installatør_underskrift': {
            'text': 'TextInPDF',
            'field': 'Underskrift',
            'type': str
        },
        'outside_specs.concrete': {
            'text': 'TextInPDF',
            'field': 'Ut Bet',
            'type': bool
        },
        'area_output': {
            'text': 'TextInPDF',
            'field': 'W/m2',
            'type': NumberTypes
        },
        'constrol_system_other_check': {
            'text': 'TextInPDF',
            'field': 'annet',
            'type': bool
        },
        'control_system_limit_sensor': {
            'text': 'TextInPDF',
            'field': 'begr',
            'type': bool
        },
        'cc': {
            'text': 'TextInPDF',
            'field': 'c/c',
            'type': NumberTypes
        },
        'control_system_floor_sensor': {
            'text': 'TextInPDF',
            'field': 'gulv',
            'type': bool
        },
        'control_system_room_sensor': {
            'text': 'TextInPDF',
            'field': 'rom',
            'type': bool
        }
    }
