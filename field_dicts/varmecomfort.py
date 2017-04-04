#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data for VarmeComfort-dictionary."""
from field_dicts import NumberTypes
varmecomfort = {
    '1': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0]',
        'type': 'topmostSubform[]'
    },
    '2': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].#field[13]',
        'type': bool
    },
    'Overdekning_betong_check': {
        'text': 'Betong check',
        'field': 'topmostSubform[0].Side1[0].#field[14]',
        'type': bool
    },
    'Overdekning_avrettermasse_check': {
        'text': 'Avrettemasse check',
        'field': 'topmostSubform[0].Side1[0].#field[15]',
        'type': bool
    },
    'Overdekning_jording_check': {
        'text': 'Jording',
        'field': 'topmostSubform[0].Side1[0].#field[16]',
        'type': bool
    },
    'Inneanlegg_lavtbyggende_brennbart_check': {
        'text': 'Lavtbyggende gulv ikke brennbart underlag',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[10]',
        'type': bool
    },
    'Inneanlegg_tradisjonell_stop_check': {
        'text': 'Tradisjonell Støp',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[11]',
        'type': bool
    },
    'Inneanlegg_annet_check': {
        'text': 'Inneanlegg annet check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[12]',
        'type': bool
    },
    'Uteanlegg_frostsikring_ror_check': {
        'text': 'Frostsikring rør',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[13]',
        'type': bool
    },
    'Uteanlegg_frostsikring_tak_check': {
        'text': 'Frostsikring tak/takrenner',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[14]',
        'type': bool
    },
    'Utenlegg_betong_check': {
        'text': 'Betong check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[15]',
        'type': bool
    },
    'Uteanlegg_belegningsstein_check': {
        'text': 'Belegninggsstein',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[16]',
        'type': bool
    },
    'Uteanlegg_annet_check': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[19]',
        'type': bool
    },
    'Uteanlegg_asfalt_check': {
        'text': 'Asdalt check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[20]',
        'type': bool
    },
    'Skisse_check': {
        'text': 'Plassering av varmenhetene er dokumentert ved Skisse side 2 check', # noqa
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[21]',
        'type': bool
    },
    'Foto_check': {
        'text': 'Plassering av varmenhetene er dokumentert ved Foto check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[22]',
        'type': bool
    },
    'Eier_informert_check': {
        'text': 'Eier og/eller bruker er informert check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[23]',
        'type': bool
    },
    'Dokumentasjon_overlevert_check': {
        'text': 'Dokumentasjonen er overlevert',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[24]',
        'type': bool
    },
    'Inneanlegg_Inteliohm_check': {
        'text': 'Inteliohm check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[25]',
        'type': bool
    },
    'Sikkerhetstiltak_Maksbegrenser_check': {
        'text': 'Maksbegrenser brukt',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[26]',
        'type': bool
    },
    'Styring_effektregulator_check': {
        'text': 'Effektregulator check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[27]',
        'type': bool
    },
    'Styring_termostat_check': {
        'text': 'Termostat',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[28]',
        'type': bool
    },
    'Styring_type_740_check': {
        'text': '740 check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[29]',
        'type': bool
    },
    'Styring_type_750_check': {
        'text': '750 check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[30]',
        'type': bool
    },
    'Styring_type_760_check': {
        'text': '760 check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[31]',
        'type': bool
    },
    'Styring_type_Annet_check': {
        'text': 'Annet check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[33]',
        'type': bool
    },
    'Styring_foler_rom_check': {
        'text': 'Romføler check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[34]',
        'type': bool
    },
    'Styring_foler_gulv_check': {
        'text': 'Gulvføler check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[35]',
        'type': bool
    },
    'Styring_foler_begrensning_check': {
        'text': 'Begrensningsføler check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[36]',
        'type': bool
    },
    'Styring_foler_annet_check': {
        'text': 'Annet check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[37]',
        'type': bool
    },
    'Styring_utendors_takrennefoler_check': {
        'text': 'Takrenneføler check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[39]',
        'type': bool
    },
    'Styring_utendors_bakkefoler_check': {
        'text': 'Bakkeføler check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[40]',
        'type': bool
    },
    'Styring_utendors_luft_check': {
        'text': 'Luftføler',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[41]',
        'type': bool
    },
    'Styring_utendors_annet_check': {
        'text': 'Annet check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[42]',
        'type': bool
    },
    'Sikkerthetstiltak_jorfdeilbryter_30ma_check': {
        'text': 'Sikkerhetstiltak jordfeilbryter 30mA innstallert',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[46]',
        'type': bool
    },
    'Sikkerhetstiltak_Temperatur_under_80_check': {
        'text': 'Temperatur i Gulv overskrider ikke 80C ved at.',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[47]',
        'type': bool
    },
    'Sikkerhetstiltak_monteringsanordning_fulgt_check': {
        'text': 'Monteringsanordning fulgt check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[48]',
        'type': bool
    },
    'Sikkerhetstiltak_eier_informert_omt_tiltak': {
        'text': 'Eier informert om tiltak',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[49]',
        'type': bool
    },
    'Inneanlegg_flxheat_kabel_check': {
        'text': 'Flxheat kabel',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[5]',
        'type': bool
    },
    'Inneanlegg_flxheat_matte_check': {
        'text': 'Flxheat mattecheck',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[6]',
        'type': bool
    },
    'Inneanlegg_lavtbyggende_ikke_brennbart_check': {
        'text': 'Lavtbyggende gulv ikke-brennbart underlag check',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[9]',
        'type': bool
    },
    'UKJENT': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text25[0]',
        'type': str
    },
    'Firma': {
        'text': 'Ansvarlig Firma',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text3[0]',
        'type': str
    },
    'Firma_org_nr': {
        'text': 'Org.nr.:',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[0]',
        'type': str
    },
    'Takrennefoler_antall': {
        'text': 'Takrenneføler antall',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[1]',
        'type': NumberTypes
    },
    'Bakkefoler_antall': {
        'text': 'Bakkeføler antall',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[2]',
        'type': NumberTypes
    },
    'Firma_adresse': {
        'text': 'dresse',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[0]',
        'type': str
    },
    'anleggs_adresse': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[1]',
        'type': str
    },
    'Produkt_inne_annet': {
        'text': 'nnet',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[2]',
        'type': str
    },
    'Produkt_ute_annet': {
        'text': 'nnet',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[3]',
        'type': str
    },
    'Styring_type_annet': {
        'text': 'nnet',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[4]',
        'type': str
    },
    'Styring_foler_annet': {
        'text': 'nnet',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[5]',
        'type': str
    },
    'Styring_utendors_annet': {
        'text': 'nnet',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[6]',
        'type': str
    },
    'Firma_telefon': {
        'text': 'Telefon',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text6[0]',
        'type': str
    },
    'Montoer': {
        'text': 'Kontaktperson',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text7[0]',
        'type': str
    },
    'Kundenavn': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text7[1]',
        'type': str
    },
    'Beskrivelse_antall': {
        'text': 'ntall',
        'field': 'topmostSubform[0].Side1[0].Text15[0]',
        'type': Takrennefoler_antall
    },
    'Beskrivelse_type_kabler': {
        'text': 'Type kabler, matter, folie',
        'field': 'topmostSubform[0].Side1[0].Text16[0]',
        'type': str
    },
    'Beskrivelse_effekt': {
        'text': 'effekt',
        'field': 'topmostSubform[0].Side1[0].Text17[0]',
        'type': NumberTypes
    },
    'Beskrivelse_ohmsk_verdi': {
        'text': 'Ideel ohmsk verdi',
        'field': 'topmostSubform[0].Side1[0].Text18[0]',
        'type': NumberTypes
    },
    'Beskrivelse_volt': {
        'text': 'Volt',
        'field': 'topmostSubform[0].Side1[0].Text19[0]',
        'type': NumberTypes
    },
    'Beskrivelse_cc': {
        'text': 'CC',
        'field': 'topmostSubform[0].Side1[0].Text20[0]',
        'type': NumberTypes
    },
    'Beskrivelse_metereffekt': {
        'text': 'W/m',
        'field': 'topmostSubform[0].Side1[0].Text21[0]',
        'type': NumberTypes
    },
    'Beskrivelse_flateeffekt': {
        'text': 'W/m2',
        'field': 'topmostSubform[0].Side1[0].Text22[0]',
        'type': NumberTypes
    },
    'Ohm_foer': {
        'text': 'Målt resistans før installasjon',
        'field': 'topmostSubform[0].Side1[0].Text23[0]',
        'type': NumberTypes
    },
    'Ohm_etter': {
        'text': 'Målt resistans etter installasjon',
        'field': 'topmostSubform[0].Side1[0].Text24[0]',
        'type': NumberTypes
    },
    'Mohm_foer': {
        'text': 'Målt isolasjon etter installasjon',
        'field': 'topmostSubform[0].Side1[0].Text25[0]',
        'type': NumberTypes
    },
    'Dato': {
        'text': 'Dato',
        'field': 'topmostSubform[0].Side1[0].Text29[0]',
        'type': str
    },
    'Underskrift': {
        'text': 'Underskrift',
        'field': 'topmostSubform[0].Side1[0].Text30[0]',
        'type': str
    },
    'Overdekning_avrettermasse_dybde': {
        'text': 'Dato',
        'field': 'topmostSubform[0].Side1[0].Text4[0]',
        'type': str
    },
    'Overdekning_betong_dybde': {
        'text': 'Dybde overdekning betong',
        'field': 'topmostSubform[0].Side1[0].Text4[1]',
        'type': str
    }

}
