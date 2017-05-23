#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for øglænd-dictionary."""
from .helpers import NumberTypes, commafloat, currentDate

translator = {
}

fields = {
    '&#197;r': {
        'text': 'TextInPDF',
        'field': '&#197;r',
        'type': bool
    },
    'Adresse Installat&#248;r': {
        'text': 'TextInPDF',
        'field': 'Adresse Installat&#248;r',
        'type': bool
    },
    'anleggs_adresse': {
        'text': 'TextInPDF',
        'field': 'Adresse installasjonssted',
        'type': 'Adresse installasjonssted'
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
    'Dag': {
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
        'type': 'Eks bad, gang'
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
        'type': 'Frostsikringsstyring type'
    },
    'produkt_type': {
        'text': 'TextInPDF',
        'field': 'Hovedgruppe',
        'type': 'Hovedgruppe'
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
    'Isolasjonstest M&#8486; inst': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest M&#8486; inst',
        'type': 'Isolasjonstest M&#; inst'
    },
    'Isolasjonstest stop': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest M&#8486; st&#248;p',
        'type': 'Isolasjonstest M&#; st&#;p'
    },
    'Isolasjonstest M&#8486; tilk': {
        'text': 'TextInPDF',
        'field': 'Isolasjonstest M&#8486; tilk',
        'type': 'Isolasjonstest M&#; tilk'
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
        'field': 'R&#248;r in',
        'type': bool
    },
    'check-utendørs-frostsikring-rør–utvendig': {
        'text': 'TextInPDF',
        'field': 'R&#248;r ut',
        'type': bool
    },
    'ohm_a': {
        'text': 'TextInPDF',
        'field': 'Resistans &#8486; inst',
        'type': NumberTypes
    },
    'ohm_b': {
        'text': 'TextInPDF',
        'field': 'Resistans &#8486; st&#248;p',
        'type': NumberTypes
    },
    'ohm_c': {
        'text': 'TextInPDF',
        'field': 'Resistans &#8486; tilk',
        'type': NumberTypes
    },
    'resistans_max': {
        'text': 'TextInPDF',
        'field': 'Resistans max &#8486;',
        'type': NumberTypes
    },
    'resistans_min': {
        'text': 'TextInPDF',
        'field': 'Resistans min &#8486;',
        'type': NumberTypes
    },
    'styring-smeltestyringstype': {
        'text': 'TextInPDF',
        'field': 'Sn&#248;smeltestyringstype',
        'type': str
    },
    'spenning': {
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
    'check-styring-annet': {
        'text': 'TextInPDF',
        'field': 'annet',
        'type': bool
    },
    'check-styring-begrensningsføler': {
        'text': 'TextInPDF',
        'field': 'begr',
        'type': bool
    },
    'cc': {
        'text': 'TextInPDF',
        'field': 'c/c',
        'type': NumberTypes
    },
    'check-styring-gulvføler': {
        'text': 'TextInPDF',
        'field': 'gulv',
        'type': bool
    },
    'check-styring-romføler': {
        'text': 'TextInPDF',
        'field': 'rom',
        'type': bool
    }

}
