#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for nexans-dictionary."""
import datetime

from .helpers import DictionaryHelper, NumberTypes, date_format
from .stamp import StampablePdfForm


class ThermoFloorCable(StampablePdfForm):

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
            'earthed_other_check': d.s_bool('earthed_other'),
            'control_system_other_check': d.s_bool('control_system_other'),
            'check-montert_i_henhold_til_installasjonsveiledning': d.s_bool('max_temp_installation')
        })
        last_date = d.g('last_date')
        if last_date:
            last_date_formatted = date_format(last_date)
            self.dict_update({
                'ohm_dato_og_underskrift': last_date_formatted,
                'mohm_dato_og_underskrift': last_date_formatted,
                'dato_spesielle_forhold': last_date_formatted,

            })

    FILL_PDF_FILENAME = 'Dokumentasjonssider_varmekabel_Ver2016-A.pdf'
    TRUE = 'Yes'
    FALSE = 'No'
    CHECKBOX_VALUE = [TRUE, FALSE]

    FIELDS_DICT = {
        'customer.address.address1': {
            'text': 'TextInPDF',
            'field': 'Adresse',
            'type':  str
        },
        'customer.address.address2': {
            'text': 'TextInPDF',
            'field': 'Adresse_2',
            'type':  str
        },
        'company.address.address1': {
            'text': 'TextInPDF',
            'field': 'Adresse_3',
            'type':  str
        },
        'Antall': {
            'text': 'TextInPDF',
            'field': 'AntallRow1',
            'type':  int
        },
        'Antall10': {
            'text': 'TextInPDF',
            'field': 'AntallRow10',
            'type':  int
        },
        'Antall2': {
            'text': 'TextInPDF',
            'field': 'AntallRow2',
            'type':  str
        },
        'Antall3': {
            'text': 'TextInPDF',
            'field': 'AntallRow3',
            'type':  str
        },
        'Antall4': {
            'text': 'TextInPDF',
            'field': 'AntallRow4',
            'type':  str
        },
        'Antall5': {
            'text': 'TextInPDF',
            'field': 'AntallRow5',
            'type':  str
        },
        'Antall6': {
            'text': 'TextInPDF',
            'field': 'AntallRow6',
            'type':  str
        },
        'Antall7': {
            'text': 'TextInPDF',
            'field': 'AntallRow7',
            'type':  str
        },
        'Antall8': {
            'text': 'TextInPDF',
            'field': 'AntallRow8',
            'type':  str
        },
        'Antall9': {
            'text': 'TextInPDF',
            'field': 'AntallRow9',
            'type':  str
        },
        'Batch': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow1',
            'type':  str
        },
        'Batch10': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow10',
            'type':  str
        },
        'Batch2': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow2',
            'type':  str
        },
        'Batch3': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow3',
            'type':  str
        },
        'Batch4': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow4',
            'type':  str
        },
        'Batch5': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow5',
            'type':  str
        },
        'Batch6': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow6',
            'type':  str
        },
        'Batch7': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow7',
            'type':  str
        },
        'Batch8': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow8',
            'type':  str
        },
        'Batch9': {
            'text': 'TextInPDF',
            'field': 'Batch nrRow9',
            'type':  str
        },
        'control_system_check_any': {
            'text': 'TextInPDF',
            'field': 'Bruk av beskyttelsesutstyr temperaturbegrenser ved feks installasjon av parkett',
            'type':  bool
        },
        'variableCheck Box5': {
            'text': 'TextInPDF',
            'field': 'Check Box5',
            'type':  bool
        },
        'variableCheck Box6': {
            'text': 'TextInPDF',
            'field': 'Check Box6',
            'type':  bool
        },
        'area_output': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row1',
            'type':  str
        },
        'area_output10': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row10',
            'type':  str
        },
        'area_output2': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row2',
            'type':  str
        },
        'area_output3': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row3',
            'type':  str
        },
        'area_output4': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row4',
            'type':  str
        },
        'area_output5': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row5',
            'type':  str
        },
        'area_output6': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row6',
            'type':  str
        },
        'area_output7': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row7',
            'type':  str
        },
        'area_output8': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row8',
            'type':  str
        },
        'area_output9': {
            'text': 'TextInPDF',
            'field': 'Effekt m²Row9',
            'type':  str
        },
        'company.name': {
            'text': 'TextInPDF',
            'field': 'Firma',
            'type':  str
        },
        'install.I': {
            'text': 'TextInPDF',
            'field': 'IRow1',
            'type':  str
        },
        'install10.I': {
            'text': 'TextInPDF',
            'field': 'IRow10',
            'type':  str
        },
        'install10_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow10_2',
            'type':  str
        },
        'install_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow1_2',
            'type':  str
        },
        'install2.I': {
            'text': 'TextInPDF',
            'field': 'IRow2',
            'type':  str
        },
        'install2_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow2_2',
            'type':  str
        },
        'install3.I': {
            'text': 'TextInPDF',
            'field': 'IRow3',
            'type':  str
        },
        'install3_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow3_2',
            'type':  str
        },
        'install4.I': {
            'text': 'TextInPDF',
            'field': 'IRow4',
            'type':  str
        },
        'install4_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow4_2',
            'type':  str
        },
        'install5.I': {
            'text': 'TextInPDF',
            'field': 'IRow5',
            'type':  str
        },
        'install5_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow5_2',
            'type':  str
        },
        'install6.I': {
            'text': 'TextInPDF',
            'field': 'IRow6',
            'type':  str
        },
        'install6_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow6_2',
            'type':  str
        },
        'install7.I': {
            'text': 'TextInPDF',
            'field': 'IRow7',
            'type':  str
        },
        'install7_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow7_2',
            'type':  str
        },
        'install8.I': {
            'text': 'TextInPDF',
            'field': 'IRow8',
            'type':  str
        },
        'install8_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow8_2',
            'type':  str
        },
        'install9.I': {
            'text': 'TextInPDF',
            'field': 'IRow9',
            'type':  str
        },
        'install9_2.I': {
            'text': 'TextInPDF',
            'field': 'IRow9_2',
            'type':  str
        },
        'check-montert_i_henhold_til_installasjonsveiledning2': {
            'text': 'TextInPDF',
            'field': 'Installasjonsveiledning for ThermoFloor gulvvarmesystemer',
            'type':  str
        },
        'installed_by': {
            'text': 'TextInPDF',
            'field': 'Installatør',
            'type':  str
        },
        'room.heated_area': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow1',
            'type':  str
        },
        'room.heated_area10': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow10',
            'type':  str
        },
        'room.heated_area2': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow2',
            'type':  str
        },
        'room.heated_area3': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow3',
            'type':  str
        },
        'room.heated_area4': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow4',
            'type':  str
        },
        'room.heated_area5': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow5',
            'type':  str
        },
        'room.heated_area6': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow6',
            'type':  str
        },
        'room.heated_area7': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow7',
            'type':  str
        },
        'room.heated_area8': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow8',
            'type':  str
        },
        'room.heated_area9': {
            'text': 'TextInPDF',
            'field': 'Installert arealRow9',
            'type':  str
        },
        'customer.contact_name': {
            'text': 'TextInPDF',
            'field': 'Kontaktperson',
            'type':  str
        },
        'customer.contact_name2': {
            'text': 'TextInPDF',
            'field': 'Kontaktperson_2',
            'type':  str
        },
        'customer.mobile': {
            'text': 'TextInPDF',
            'field': 'Mobil',
            'type':  str
        },
        'customer.mobile@': {
            'text': 'TextInPDF',
            'field': 'Mobil_2',
            'type':  str
        },
        'company.mobile': {
            'text': 'TextInPDF',
            'field': 'Mobil_3',
            'type':  str
        },
        'max_temp_installation': {
            'text': 'TextInPDF',
            'field': 'Montasjen av oppvarmingssystemet',
            'type':  str
        },
        'customer.name': {
            'text': 'TextInPDF',
            'field': 'Navn',
            'type':  str
        },
        'customer.name2': {
            'text': 'TextInPDF',
            'field': 'Navn_2',
            'type':  str
        },
        'variableNominativt tillegg 753A': {
            'text': 'TextInPDF',
            'field': 'Nominativt tillegg 753A',
            'type':  str
        },
        'customer.orgnumber_f': {
            'text': 'TextInPDF',
            'field': 'Org nr',
            'type':  str
        },
        'customer.orgnumber2_f': {
            'text': 'TextInPDF',
            'field': 'Org nr_2',
            'type':  str
        },
        'company.orgnumber_f': {
            'text': 'TextInPDF',
            'field': 'Org nr_3',
            'type':  str
        },
        'max_temp_planning': {
            'text': 'TextInPDF',
            'field': 'Planlegging av oppvarmingssystemet',
            'type':  str
        },
        'customer.address.post_code': {
            'text': 'TextInPDF',
            'field': 'Postnummer',
            'type':  str
        },
        'customer.address2.post_code': {
            'text': 'TextInPDF',
            'field': 'Postnummer_2',
            'type':  str
        },
        'company.address.post_code': {
            'text': 'TextInPDF',
            'field': 'Postnummer_3',
            'type':  str
        },
        'customer.address.post_area': {
            'text': 'TextInPDF',
            'field': 'Poststed',
            'type':  str
        },
        'customer.address2.post_area': {
            'text': 'TextInPDF',
            'field': 'Poststed_2',
            'type':  str
        },
        'company.address.post_area': {
            'text': 'TextInPDF',
            'field': 'Poststed_3',
            'type':  str
        },
        'room.name': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow1',
            'type':  str
        },
        'room.name10': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow10',
            'type':  str
        },
        'room.name10_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow10_2',
            'type':  str
        },
        'room.name_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow1_2',
            'type':  str
        },
        'room.name2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow2',
            'type':  str
        },
        'room.name2_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow2_2',
            'type':  str
        },
        'room.name3': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow3',
            'type':  str
        },
        'room.name3_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow3_2',
            'type':  str
        },
        'room.name4': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow4',
            'type':  str
        },
        'room.name4_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow4_2',
            'type':  str
        },
        'room.name5': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow5',
            'type':  str
        },
        'room.name5_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow5_2',
            'type':  str
        },
        'room.name6': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow6',
            'type':  str
        },
        'room.name6_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow6_2',
            'type':  str
        },
        'room.name7': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow7',
            'type':  str
        },
        'room.name7_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow7_2',
            'type':  str
        },
        'room.name8': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow8',
            'type':  str
        },
        'room.name8_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow8_2',
            'type':  str
        },
        'room.name9': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow9',
            'type':  str
        },
        'room.name9_2': {
            'text': 'TextInPDF',
            'field': 'Rom angi typeRow9_2',
            'type':  str
        },
        'company.contact_name': {
            'text': 'TextInPDF',
            'field': 'Saksbehandler',
            'type':  str
        },
        'customer.phone': {
            'text': 'TextInPDF',
            'field': 'Telefon',
            'type':  str
        },
        'customer.phone2': {
            'text': 'TextInPDF',
            'field': 'Telefon2',
            'type':  str
        },
        'company.contact_phone_f': {
            'text': 'TextInPDF',
            'field': 'Telefon3',
            'type':  str
        },
        'installation_depth_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow1',
            'type':  str
        },
        'installation_depth10_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow10',
            'type':  str
        },
        'installation_depth2_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow2',
            'type':  str
        },
        'installation_depth3_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow3',
            'type':  str
        },
        'installation_depth4_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow4',
            'type':  str
        },
        'installation_depth5_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow5',
            'type':  str
        },
        'installation_depth6_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow6',
            'type':  str
        },
        'installation_depth7_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow7',
            'type':  str
        },
        'installation_depth8_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow8',
            'type':  str
        },
        'installation_depth9_2': {
            'text': 'TextInPDF',
            'field': 'Tykkelse overdekkingRow9',
            'type':  str
        },
        'pour_type': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow1',
            'type':  str
        },
        'pour_type10': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow10',
            'type':  str
        },
        'pour_type2': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow2',
            'type':  str
        },
        'pour_type3': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow3',
            'type':  str
        },
        'pour_type4': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow4',
            'type':  str
        },
        'pour_type5': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow5',
            'type':  str
        },
        'pour_type6': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow6',
            'type':  str
        },
        'pour_type7': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow7',
            'type':  str
        },
        'pour_type8': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow8',
            'type':  str
        },
        'pour_type9': {
            'text': 'TextInPDF',
            'field': 'Type overdekkingRow9',
            'type':  str
        },
        'floor_type': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow1',
            'type':  str
        },
        'floor_type10': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow10',
            'type':  str
        },
        'floor_type2': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow2',
            'type':  str
        },
        'floor_type3': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow3',
            'type':  str
        },
        'floor_type4': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow4',
            'type':  str
        },
        'floor_type5': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow5',
            'type':  str
        },
        'floor_type6': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow6',
            'type':  str
        },
        'floor_type7': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow7',
            'type':  str
        },
        'floor_type8': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow8',
            'type':  str
        },
        'floor_type9': {
            'text': 'TextInPDF',
            'field': 'Type undergulvRow9',
            'type':  str
        },
        'product.name': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow1',
            'type':  str
        },
        'product.name10': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow10',
            'type':  str
        },
        'product.name2': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow2',
            'type':  str
        },
        'product.name3': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow3',
            'type':  str
        },
        'product.name4': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow4',
            'type':  str
        },
        'product.name5': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow5',
            'type':  str
        },
        'product.name6': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow6',
            'type':  str
        },
        'product.name7': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow7',
            'type':  str
        },
        'product.name8': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow8',
            'type':  str
        },
        'product.name9': {
            'text': 'TextInPDF',
            'field': 'Type varmeenhetRow9',
            'type':  str
        },
        'check-montert_i_henhold_til_installasjonsveiledning': {
            'text': 'TextInPDF',
            'field': 'Utført i hht krav i installasjonsveiledningen',
            'type':  bool
        },
        'fuck': {
            'text': 'TextInPDF',
            'field': 'Utvidelseendring av eksisterende anlegg',
            'type':  bool
        },
        'variableVedlagt bilder med oppvarmet område': {
            'text': 'TextInPDF',
            'field': 'Vedlagt bilder med oppvarmet område',
            'type':  str
        },
        'variableVedlegg': {
            'text': 'TextInPDF',
            'field': 'Vedlegg',
            'type':  str
        },
        'install9.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_102',
            'type':  str
        },
        'install9_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_102_2',
            'type':  str
        },
        'install9.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_103',
            'type':  str
        },
        'install10.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_109',
            'type':  str
        },
        'install10.mohm_2': {
            'text': 'TextInPDF',
            'field': 'fill_109_2',
            'type':  str
        },
        'install11.ohm0': {
            'text': 'TextInPDF',
            'field': 'fill_110',
            'type':  str
        },
        'install_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_113',
            'type':  str
        },
        'install2_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_116',
            'type':  str
        },
        'install3_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_119',
            'type':  str
        },
        'install4_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_122',
            'type':  str
        },
        'install5_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_125',
            'type':  str
        },
        'install6_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_128',
            'type':  str
        },
        'install7_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_131',
            'type':  str
        },
        'install8_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_134',
            'type':  str
        },
        'install9_2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_137',
            'type':  str
        },
        'install10.ohm_2': {
            'text': 'TextInPDF',
            'field': 'fill_140',
            'type':  str
        },
        'install.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_46',
            'type':  str
        },
        'install_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_46_2',
            'type':  str
        },
        'install.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_47',
            'type':  str
        },
        'install2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_53',
            'type':  str
        },
        'install2_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_53_2',
            'type':  str
        },
        'install2.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_54',
            'type':  str
        },
        'install3.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_60',
            'type':  str
        },
        'install3_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_60_2',
            'type':  str
        },
        'install3.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_61',
            'type':  str
        },
        'install4.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_67',
            'type':  str
        },
        'install4_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_67_2',
            'type':  str
        },
        'install4.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_68',
            'type':  str
        },
        'install5.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_74',
            'type':  str
        },
        'install5_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_74_2',
            'type':  str
        },
        'install5.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_75',
            'type':  str
        },
        'install6.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_81',
            'type':  str
        },
        'install6_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_81_2',
            'type':  str
        },
        'install6.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_82',
            'type':  str
        },
        'install7.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_88',
            'type':  str
        },
        'install7_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_88_2',
            'type':  str
        },
        'install7.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_89',
            'type':  str
        },
        'install8.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_95',
            'type':  str
        },
        'install8_2.mohm': {
            'text': 'TextInPDF',
            'field': 'fill_95_2',
            'type':  str
        },
        'install8.ohm': {
            'text': 'TextInPDF',
            'field': 'fill_96',
            'type':  str
        },
        'number_of_attachments': {
            'text': 'TextInPDF',
            'field': 'stk',
            'type':  str
        },
        'variableundefined': {
            'text': 'TextInPDF',
            'field': 'undefined',
            'type':  str
        },
        'variableundefined_10': {
            'text': 'TextInPDF',
            'field': 'undefined_10',
            'type':  str
        },
        'variableundefined_11': {
            'text': 'TextInPDF',
            'field': 'undefined_11',
            'type':  str
        },
        'variableundefined_2': {
            'text': 'TextInPDF',
            'field': 'undefined_2',
            'type':  str
        },
        'variableundefined_3': {
            'text': 'TextInPDF',
            'field': 'undefined_3',
            'type':  str
        },
        'variableundefined_8': {
            'text': 'TextInPDF',
            'field': 'undefined_8',
            'type':  str
        },
        'variableundefined_9': {
            'text': 'TextInPDF',
            'field': 'undefined_9',
            'type':  str
        }

    }
