#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for nexans-dictionary."""
from .helpers import (DictionaryHelper, NumberTypes,
                      group_number, month_name, date_format)
from .stamp import StampablePdfForm, signatere_location_size
from dateutil.parser import parse


class Nexans(StampablePdfForm):

    def __init__(self, dictionary):
        super().__init__(
            dictionary=dictionary,
            fill_pdf_filename=self.FILL_PDF_FILENAME,
            fields_dict=self.FIELDS_DICT,
            checkbox_value=self.CHECKBOX_VALUE,
            signature_location_sizes=[
                {
                    'x': 164,
                    'y': 176,
                    'w': 219,
                    'h': 19
                },
                {
                    'x': 174,
                    'y': 432,
                    'w': 114,
                    'h': 16
                },
                {
                    'x': 174,
                    'y': 524,
                    'w': 114,
                    'h': 16
                }
            ])
        from pprint import pprint
        pprint(dictionary)

    def translate(self):

        d = DictionaryHelper(self.dictionary)
        self.dict_update({
            'anleggs_adresse2':
                d.s_if('customer.address.address2', sub=', ') +
                d.s_if('customer.address.post_code', sub=' ') +
                d.s('customer.address.post_area'),
            'type_og_effekt':
                ', '.join([
                    d.s('product.product_type.name'),
                    d.s_if('product.effect', sub='W'),
                ]),
            'product.resistance_nominal': '{0:.1f}'.format(
                    d.g('product.resistance_nominal')
                    ),
            'check-toleder': not d.s_bool('product.twowires'),
            'check-enleder': d.s_bool('product.twowires'),
            'max_temp_other_check': d.s_bool('max_temp_other'),
            'earthed_other_check': d.s_bool('earthed_other')
        })

        pour_date = d.g('pour.date')
        install_date = d.g('install.date')
        connect_date = d.g('connect.date')
        last_date = None
        for date in [pour_date, install_date, connect_date]:
            if date:
                parsed = parse(date)
                if parsed and not last_date or parsed > last_date:
                    last_date = parsed
        if pour_date:
            self.dict_update({
                'pour.date.formatted': date_format(parse(pour_date))
            })
        if last_date:
            last_date_formatted = date_format(last_date)
            self.dict_update({
                'ohm_dato_og_underskrift': last_date_formatted,
                'mohm_dato_og_underskrift': last_date_formatted,
                'dato_spesielle_forhold': last_date_formatted,

            })

    FILL_PDF_FILENAME = '2012_Garantiskjema_V2_varmekabel_Nexans Norway.pdf'
    TRUE = 'Yes'
    FALSE = 'No'
    CHECKBOX_VALUE = [TRUE, FALSE]

    FIELDS_DICT = {
        'check-enleder': {
            'text': 'TextInPDF',
            'field': 'Check Box1',
            'type': bool
        },
        'check-toleder': {
            'text': 'TextInPDF',
            'field': 'Check Box2',
            'type': bool
        },
        'earthed_cable_screen': {
            'text': 'TextInPDF',
            'field': 'Check Box3',
            'type': bool
        },
        'earthed_chicken_wire': {
            'text': 'TextInPDF',
            'field': 'Check Box4',
            'type': bool
        },
        'earthed_other_check': {
            'text': 'TextInPDF',
            'field': 'Check Box5',
            'type': bool
        },
        'check-montert_i_henhold_til_installasjonsveiledning': {
            'text': 'TextInPDF',
            'field': 'Check Box6',
            'type': bool
        },
        'check-ikke_montert_i_henhold_til_installasjonsveiledning': {
            'text': 'TextInPDF',
            'field': 'Check Box7',
            'type': bool
        },
        'max_temp_planning': {
            'text': 'TextInPDF',
            'field': 'Check Box8',
            'type': bool
        },
        'max_temp_installation': {
            'text': 'TextInPDF',
            'field': 'Check Box9',
            'type': bool
        },
        'max_temp_other_check': {
            'text': 'TextInPDF',
            'field': 'Check Box10',
            'type': bool
        },
        'control_system_floor_sensor': {
            'text': 'TextInPDF',
            'field': 'Check Box11',
            'type': bool
        },
        'control_system_room_sensor': {
            'text': 'TextInPDF',
            'field': 'Check Box12',
            'type': bool
        },
        'control_system_other_check': {
            'text': 'TextInPDF',
            'field': 'Check Box13',
            'type': bool
        },
        'company.name': {
            'text': 'Installert av (firma)',
            'field': 'Text1',
            'type': str
        },
        'customer.address.address1': {
            'text': 'Innstalleringsadresse',
            'field': 'Text2',
            'type': str
        },
        'anleggs_adresse2': {
            'text': 'Innstalleringsadresse',
            'field': 'Text3',
            'type': str
        },
        'room.name': {
            'text': 'Rom',
            'field': 'Text4',
            'type': str
        },
        'room.area': {
            'text': 'Areal',
            'field': 'Text5',
            'type': NumberTypes
        },
        'type_og_effekt': {
            'text': 'Typebetegnelse og effekt',
            'field': 'Text6',
            'type': str
        },
        'product.watt_per_(square)_meter': {
            'text': 'Metereffekt',
            'field': 'Text7',
            'type': NumberTypes
        },
        'product.resistance_nominal': {
            'text': 'Nominell motstand',
            'field': 'Text8',
            'type': NumberTypes
        },
        'product.voltage': {
            'text': 'Driftspenning',
            'field': 'Text9',
            'type': NumberTypes
        },
        'install.ohm': {
            'text': 'TextInPDF',
            'field': 'Text10',
            'type': str
        },
        'pour.ohm': {
            'text': 'TextInPDF',
            'field': 'Text11',
            'type': str
        },
        'connect.ohm': {
            'text': 'TextInPDF',
            'field': 'Text12',
            'type': str
        },
        'ohm_dato_og_underskrift': {
            'text': 'TextInPDF',
            'field': 'Text13',
            'type': str
        },
        'install.mohm': {
            'text': 'TextInPDF',
            'field': 'Text14',
            'type': str
        },
        'pour.mohm': {
            'text': 'TextInPDF',
            'field': 'Text15',
            'type': str
        },
        'connect.mohm': {
            'text': 'TextInPDF',
            'field': 'Text16',
            'type': str
        },
        'montasjedybde': {
            'text': 'TextInPDF',
            'field': 'Text17',
            'type': str
        },
        # antall_elementer_matter_installert
        'room.product_count': {
            'text': 'TextInPDF',
            'field': 'Text18',
            'type': str
        },
        'room.heated_area': {
            'text': 'TextInPDF',
            'field': 'Text19',
            'type': str
        },
        'area_output': {
            'text': 'TextInPDF',
            'field': 'Text20',
            'type': str
        },
        'sikringstørrelse': {
            'text': 'TextInPDF',
            'field': 'Text21',
            'type': str
        },
        'utløserstrøm_for_fordfeilvern': {
            'text': 'TextInPDF',
            'field': 'Text22',
            'type': str
        },
        'mohm_dato_og_underskrift': {
            'text': 'TextInPDF',
            'field': 'Text23',
            'type': str
        },
        'earthed_other': {
            'text': 'TextInPDF',
            'field': 'Text24',
            'type': str
        },
        'spesielle_forhold': {
            'text': 'TextInPDF',
            'field': 'Text25',
            'type': str
        },
        'underskrift_installatør': {
            'text': 'TextInPDF',
            'field': 'Text26',
            'type': str
        },
        'stempel_installatør': {
            'text': 'TextInPDF',
            'field': 'Text27',
            'type': str
        },
        'støpemasse_benyttet': {
            'text': 'TextInPDF',
            'field': 'Text28',
            'type': str
        },
        'dato_spesielle_forhold': {
            'text': 'TextInPDF',
            'field': 'Text29',
            'type': str
        },
        'støpetykkelse_støper': {
            'text': 'TextInPDF',
            'field': 'Text30',
            'type': str
        },
        'pour.date.formatted': {
            'text': 'TextInPDF',
            'field': 'Text31',
            'type': str
        },
        'underskrift_støper': {
            'text': 'TextInPDF',
            'field': 'Text32',
            'type': str
        },
        'underskrift_anleggseier': {
            'text': 'TextInPDF',
            'field': 'Text33',
            'type': str
        },
        'dat_anleggseier': {
            'text': 'TextInPDF',
            'field': 'Text34',
            'type': str
        },
        'max_temp_other': {
            'text': 'TextInPDF',
            'field': 'Text35',
            'type': str
        },
        'control_system_type': {
            'text': 'TextInPDF',
            'field': 'Text36',
            'type': str
        },
        'control_system_other': {
            'text': 'TextInPDF',
            'field': 'Text37',
            'type': str
        }
    }
