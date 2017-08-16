#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for nexans-dictionary."""
from .helpers import NumberTypes, commafloat, currentDate
pdf_path = 'static/forms/2012_Garantiskjema_V2_varmekabel_Nexans Norway.pdf'

signature_location_size = [
    {
        'x': 164,
        'y': 176,
        'sizex': 219,
        'sizey': 19
    },
    {
        'x': 174,
        'y': 432,
        'sizex': 114,
        'sizey': 16
    },
    {
        'x': 174,
        'y': 524,
        'sizex': 114,
        'sizey': 16
    }
]


translator = {
    'type_og_effekt': [
        '{}',
        lambda x: (x['Betegnelse'],)
    ],
    'flateeffekt': [
        '{:.2f}',
        lambda x: (commafloat(x['effekt']) / commafloat(x['oppvarmet_areal']),)
    ],
    'anleggs_adresse2': [
        '{} {}',
        lambda x: (x['anleggs_postnummer'], x['anleggs_poststed'])
    ],
    'ohm_dato_og_underskrift': [
        '{}',
        lambda x: (currentDate(),)
    ],
    'mohm_dato_og_underskrift': [
        '{}',
        lambda x: (currentDate(),)
    ],
    'dato_spesielle_forhold': [
        '{}',
        lambda x: (currentDate(),)
    ],
    'mohm_a': [
        '{}',
        lambda x: ('999' if x['mohm_a'] == 'true' else '',)
    ],
    'mohm_b': [
        '{}',
        lambda x: ('999' if x['mohm_b'] == 'true' else '',)
    ],
    'mohm_c': [
        '{}',
        lambda x: ('999' if x['mohm_c'] == 'true' else '',)
    ],

}

yes = 'Yes'
no = 'No'

checkbox_value = [yes, no]

fields_dict = {
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
    'check-jordet_kabelskjerm': {
        'text': 'TextInPDF',
        'field': 'Check Box3',
        'type': bool
    },
    'check-jordet_netting': {
        'text': 'TextInPDF',
        'field': 'Check Box4',
        'type': bool
    },
    'check-jording_annet': {
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
    'check-maks_temp_planlegging': {
        'text': 'TextInPDF',
        'field': 'Check Box8',
        'type': bool
    },
    'check-maks_temp_utførelse': {
        'text': 'TextInPDF',
        'field': 'Check Box9',
        'type': bool
    },
    'check-maks_temp_annet': {
        'text': 'TextInPDF',
        'field': 'Check Box10',
        'type': bool
    },
    'check-følertype-gulv': {
        'text': 'TextInPDF',
        'field': 'Check Box11',
        'type': bool
    },
    'check-følertype-rom': {
        'text': 'TextInPDF',
        'field': 'Check Box12',
        'type': bool
    },
    'check-følertype-annet': {
        'text': 'TextInPDF',
        'field': 'Check Box13',
        'type': bool
    },
    'firma_navn': {
        'text': 'Installert av (firma)',
        'field': 'Text1',
        'type': str
    },
    'anleggs_adresse1': {
        'text': 'Innstalleringsadresse',
        'field': 'Text2',
        'type': str
    },
    'anleggs_adresse2': {
        'text': 'Innstalleringsadresse',
        'field': 'Text3',
        'type': str
    },
    'rom_navn': {
        'text': 'Rom',
        'field': 'Text4',
        'type': str
    },
    'areal': {
        'text': 'Areal',
        'field': 'Text5',
        'type': NumberTypes
    },
    'type_og_effekt': {
        'text': 'Typebetegnelse og effekt',
        'field': 'Text6',
        'type': str
    },
    'meterEffekt': {
        'text': 'Metereffekt',
        'field': 'Text7',
        'type': NumberTypes
    },
    'nominell_motstand': {
        'text': 'Nominell motstand',
        'field': 'Text8',
        'type': NumberTypes
    },
    'driftspenning': {
        'text': 'Driftspenning',
        'field': 'Text9',
        'type': NumberTypes
    },
    'ohm_a': {
        'text': 'TextInPDF',
        'field': 'Text10',
        'type': str
    },
    'ohm_b': {
        'text': 'TextInPDF',
        'field': 'Text11',
        'type': str
    },
    'ohm_c': {
        'text': 'TextInPDF',
        'field': 'Text12',
        'type': str
    },
    'ohm_dato_og_underskrift': {
        'text': 'TextInPDF',
        'field': 'Text13',
        'type': str
    },
    'mohm_a': {
        'text': 'TextInPDF',
        'field': 'Text14',
        'type': str
    },
    'mohm_b': {
        'text': 'TextInPDF',
        'field': 'Text15',
        'type': str
    },
    'mohm_c': {
        'text': 'TextInPDF',
        'field': 'Text16',
        'type': str
    },
    'montasjedybde': {
        'text': 'TextInPDF',
        'field': 'Text17',
        'type': str
    },
    'antall_elementer_matter_installert': {
        'text': 'TextInPDF',
        'field': 'Text18',
        'type': str
    },
    'oppvarmet_areal': {
        'text': 'TextInPDF',
        'field': 'Text19',
        'type': str
    },
    'flateeffekt': {
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
    'jording_annet': {
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
    'dato_støper': {
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
    'maks_temp_beskrivelse': {
        'text': 'TextInPDF',
        'field': 'Text35',
        'type': str
    },
    'styresystem_typebetegnelse': {
        'text': 'TextInPDF',
        'field': 'Text36',
        'type': str
    },
    'følertype_annet': {
        'text': 'TextInPDF',
        'field': 'Text37',
        'type': str
    }
}
