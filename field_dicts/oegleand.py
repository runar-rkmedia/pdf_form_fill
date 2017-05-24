#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for øglænd-dictionary."""
from .helpers import NumberTypes, commafloat, currentDate

translator = {
    'check-jordfeilbryter-30mA': [
        '{}',
        lambda x: yes if x['utløserstrøm_for_fordfeilvern'] else no
    ],
    'check-beskyttelses-tiltak-monteringsanvisning-fulgt': [
        '{}',
        lambda x: yes if x[
            'check-installasjonsveiledning_fulgt'] else no
    ],
    'check-beskyttelses-tiltak-bruk-av-styring': [
        '{}',
        lambda x: yes if x[
            'check-følertype-gulv'] or x[
                'check-følertype-rom'] or x[
                    'check-følertype-begrensningsføler'] or x[
                        'check-følertype-annet'] else no
    ],
}

yes = 'Ja'
no = 'Nei'

checkbox_value = [yes, no]

fields = {
    'dato-År': {
        'text': 'TextInPDF',
        'field': 'År',
        'type': str
    },
    'firma_adresse': {
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
    'oppvarmet_areal': {
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
        'type': bool
    },
    'Doku': {
        'text': 'TextInPDF',
        'field': 'Doku',
        'type': bool
    },
    'effekt': {
        'text': 'TextInPDF',
        'field': 'Effekt W',
        'type': str
    },
    'Eier': {
        'text': 'TextInPDF',
        'field': 'Eier',
        'type': bool
    },
    'rom_navn': {
        'text': 'TextInPDF',
        'field': 'Eks bad, gang',
        'type': str
    },
    'Fart': {
        'text': 'TextInPDF',
        'field': 'Fart',
        'type': bool
    },
    'firma_navn': {
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
    'produkt_type': {
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
    'm_ohm': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest MΩ inst',
        'type': str
    },
    'Isolasjonstest stop': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest MΩ støp',
        'type': str
    },
    'Isolasjonstest MΩ tilk': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest MΩ tilk',
        'type': str
    },
    'check-jordfeilbryter-30mA': {
        'text': 'TextInPDF',
        'field': 'Jord',
        'type': bool
    },
    'firma_kontaktperson': {
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
        'type': NumberTypes
    },
    'check-beskyttelses-tiltak-monteringsanvisning-fulgt': {
        'text': 'TextInPDF',
        'field': 'Mont',
        'type': bool
    },
    'firma_orgnr': {
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
    'resistans_max': {
        'text': 'TextInPDF',
        'field': 'Resistans max Ω',
        'type': NumberTypes
    },
    'resistans_min': {
        'text': 'TextInPDF',
        'field': 'Resistans min Ω',
        'type': NumberTypes
    },
    'styring-smeltestyringstype': {
        'text': 'TextInPDF',
        'field': 'Snøsmeltestyringstype',
        'type': str
    },
    'driftspenning': {
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
    'firma_telefon': {
        'text': 'TextInPDF',
        'field': 'Telefon',
        'type': str
    },
    'type_kabel_matte': {
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
