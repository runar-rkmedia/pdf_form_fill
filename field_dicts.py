"""part of smart pdf filler."""
# import types
# python2
# NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
NumberTypes = (int, float, complex)

nexans = {
    'variableCheck Box1': {
        'text': 'TextInPDF',
        'field': 'Check Box1',
        'type': bool
    },
    'variableCheck Box2': {
        'text': 'TextInPDF',
        'field': 'Check Box2',
        'type': bool
    },
    'variableCheck Box3': {
        'text': 'TextInPDF',
        'field': 'Check Box3',
        'type': bool
    },
    'variableCheck Box4': {
        'text': 'TextInPDF',
        'field': 'Check Box4',
        'type': bool
    },
    'variableCheck Box5': {
        'text': 'TextInPDF',
        'field': 'Check Box5',
        'type': bool
    },
    'variableCheck Box6': {
        'text': 'TextInPDF',
        'field': 'Check Box6',
        'type': bool
    },
    'variableCheck Box7': {
        'text': 'TextInPDF',
        'field': 'Check Box7',
        'type': bool
    },
    'variableCheck Box8': {
        'text': 'TextInPDF',
        'field': 'Check Box8',
        'type': bool
    },
    'variableCheck Box9': {
        'text': 'TextInPDF',
        'field': 'Check Box9',
        'type': bool
    },
    'variableCheck Box10': {
        'text': 'TextInPDF',
        'field': 'Check Box10',
        'type': bool
    },
    'variableCheck Box11': {
        'text': 'TextInPDF',
        'field': 'Check Box11',
        'type': bool
    },
    'variableCheck Box12': {
        'text': 'TextInPDF',
        'field': 'Check Box12',
        'type': bool
    },
    'variableCheck Box13': {
        'text': 'TextInPDF',
        'field': 'Check Box13',
        'type': bool
    },
    'firma_navn': {
        'text': 'Installert av (firma)',
        'field': 'Text1',
        'type': str
    },
    'anleggs_adresse': {
        'text': 'Innstalleringsadresse',
        'field': 'Text2',
        'type': str
    },
    'anleggs_adresse2': {
        'text': 'Innstalleringsadresse',
        'field': 'Text3',
        'type': str
    },
    'Rom_navn': {
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
    'variableText10': {
        'text': 'TextInPDF',
        'field': 'Text10',
        'type': str
    },
    'variableText11': {
        'text': 'TextInPDF',
        'field': 'Text11',
        'type': str
    },
    'variableText12': {
        'text': 'TextInPDF',
        'field': 'Text12',
        'type': str
    },
    'variableText13': {
        'text': 'TextInPDF',
        'field': 'Text13',
        'type': str
    },
    'variableText14': {
        'text': 'TextInPDF',
        'field': 'Text14',
        'type': str
    },
    'variableText15': {
        'text': 'TextInPDF',
        'field': 'Text15',
        'type': str
    },
    'variableText16': {
        'text': 'TextInPDF',
        'field': 'Text16',
        'type': str
    },
    'variableText17': {
        'text': 'TextInPDF',
        'field': 'Text17',
        'type': str
    },
    'variableText18': {
        'text': 'TextInPDF',
        'field': 'Text18',
        'type': str
    },
    'variableText19': {
        'text': 'TextInPDF',
        'field': 'Text19',
        'type': str
    },
    'variableText20': {
        'text': 'TextInPDF',
        'field': 'Text20',
        'type': str
    },
    'variableText21': {
        'text': 'TextInPDF',
        'field': 'Text21',
        'type': str
    },
    'variableText22': {
        'text': 'TextInPDF',
        'field': 'Text22',
        'type': str
    },
    'variableText23': {
        'text': 'TextInPDF',
        'field': 'Text23',
        'type': str
    },
    'variableText24': {
        'text': 'TextInPDF',
        'field': 'Text24',
        'type': str
    },
    'variableText25': {
        'text': 'TextInPDF',
        'field': 'Text25',
        'type': str
    },
    'variableText26': {
        'text': 'TextInPDF',
        'field': 'Text26',
        'type': str
    },
    'variableText27': {
        'text': 'TextInPDF',
        'field': 'Text27',
        'type': str
    },
    'variableText28': {
        'text': 'TextInPDF',
        'field': 'Text28',
        'type': str
    },
    'variableText29': {
        'text': 'TextInPDF',
        'field': 'Text29',
        'type': str
    },
    'variableText30': {
        'text': 'TextInPDF',
        'field': 'Text30',
        'type': str
    },
    'variableText31': {
        'text': 'TextInPDF',
        'field': 'Text31',
        'type': str
    },
    'variableText32': {
        'text': 'TextInPDF',
        'field': 'Text32',
        'type': str
    },
    'variableText33': {
        'text': 'TextInPDF',
        'field': 'Text33',
        'type': str
    },
    'variableText34': {
        'text': 'TextInPDF',
        'field': 'Text34',
        'type': str
    },
    'variableText35': {
        'text': 'TextInPDF',
        'field': 'Text35',
        'type': str
    },
    'variableText36': {
        'text': 'TextInPDF',
        'field': 'Text36',
        'type': str
    },
    'variableText37': {
        'text': 'TextInPDF',
        'field': 'Text37',
        'type': str
    }
}
varmecomfort = {
    'variabletopmostSubform[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0]',
        'type': 'topmostSubform[]'
    },
    'variabletopmostSubform[0].Side1[0].#field[13]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].#field[13]',
        'type': 'topmostSubform[].Side[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].#field[14]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].#field[14]',
        'type': 'topmostSubform[].Side[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].#field[15]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].#field[15]',
        'type': 'topmostSubform[].Side[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].#field[16]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].#field[16]',
        'type': 'topmostSubform[].Side[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[10]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[10]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[11]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[11]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[12]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[12]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[13]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[13]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[14]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[14]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[15]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[15]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[16]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[16]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[19]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[19]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[20]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[20]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[21]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[21]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[22]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[22]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[23]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[23]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[24]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[24]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[25]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[25]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[26]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[26]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[27]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[27]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[28]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[28]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[29]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[29]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[30]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[30]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[31]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[31]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[33]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[33]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[34]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[34]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[35]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[35]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[36]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[36]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[37]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[37]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[39]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[39]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[40]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[40]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[41]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[41]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[42]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[42]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[46]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[46]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[47]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[47]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[48]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[48]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[49]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[49]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[5]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[5]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[6]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[6]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].#field[9]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].#field[9]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].#field[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text25[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text25[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text3[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text3[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text4[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text4[1]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[1]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text4[2]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text4[2]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[1]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[1]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[2]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[2]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[3]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[3]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[4]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[4]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[5]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[5]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text5[6]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text5[6]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text6[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text6[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text7[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text7[0]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].PlacedPDF[0].Text7[1]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].PlacedPDF[0].Text7[1]',
        'type': 'topmostSubform[].Side[].PlacedPDF[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text15[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text15[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text16[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text16[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text17[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text17[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text18[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text18[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text19[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text19[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text20[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text20[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text21[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text21[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text22[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text22[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text23[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text23[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text24[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text24[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text25[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text25[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text29[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text29[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text30[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text30[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text4[0]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text4[0]',
        'type': 'topmostSubform[].Side[].Text[]'
    },
    'variabletopmostSubform[0].Side1[0].Text4[1]': {
        'text': 'TextInPDF',
        'field': 'topmostSubform[0].Side1[0].Text4[1]',
        'type': 'topmostSubform[].Side[].Text[]'
    }

}
