"""Forms used for HTML.."""
# -*- coding: utf-8 -*-
import decimal

from flask_wtf import FlaskForm
from wtforms import IntegerField as baseIntegerField  # RadioField,
from wtforms import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    StringField
)
from wtforms.fields.html5 import (
    DateField,
    DecimalField,
    EmailField,
    IntegerField,
    TelField
)
from wtforms.validators import NumberRange  # Email,
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError
)
from wtforms.widgets import HiddenInput
from wtforms_html5 import AutoAttrMeta


class Unique(object):
    """ validator that checks field uniqueness """

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class SubForm(FlaskForm):
    """CsrfToken-basic."""

    def __init__(self, **_kwargs):
        _kwargs['csrf_enabled'] = False
        super().__init__(**_kwargs)


class HiddenInteger(baseIntegerField):
    widget = HiddenInput()


# https://stackoverflow.com/a/35359450/3493586


class BetterDecimalField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    """

    def __init__(self,
                 label=None,
                 validators=None,
                 places=2,
                 rounding=None,
                 round_always=True,
                 **kwargs):
        super(BetterDecimalField, self).__init__(
            label=label,
            validators=validators,
            places=places,
            rounding=rounding,
            **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1')**self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value'))


class CheckMaxTemp(SubForm):
    planning = BooleanField(
        'Planlegging (innstallasjonsveiledningen er fulgt, og eier er informert om forutsetningene)'  # noqa
    )
    installation = BooleanField(
        'Utførelse av montasje (Installasjonsveiledningen er fulgt)'  # noqa
    )
    other = StringField(
        'Eventuell bruk av beskyttelsesutstyr',  # noqa
        validators=[Length(max=100)])


class CheckEarthed(SubForm):
    cable_screen = BooleanField('Jordet kabelskjerm')
    chicken_wire = BooleanField('Jordet netting')
    other = StringField('Annet', validators=[Length(max=100)])


class CheckControlSystem(SubForm):
    floor_sensor = BooleanField('Gulv')
    room_sensor = BooleanField('Rom')
    limit_sensor = BooleanField('Begrensning')
    designation = StringField(
        'Typebetegnelse',  # noqa
        validators=[Length(max=50)])
    other = StringField(
        'Annet',  # noqa
        validators=[Length(max=100)])


frost_protection_pipe = BooleanField('Frostsikring rør')


class HeatingInside(SubForm):
    LamiFlex = BooleanField('ØS Lamiflex')
    low_profile = BooleanField('Lavtbyggende gulv')
    fireproof = BooleanField('Brennbart underlag')
    frost_protection_pipe = frost_protection_pipe
    other = StringField('Annet', validators=[Length(max=100)])
    concrete = BooleanField('Betong')


class HeatingOutside(SubForm):
    asphalt = BooleanField('Asfalt')
    paving_stones = BooleanField('Belegningsstein')
    vessel = BooleanField('Fartøy')
    frost_protection = BooleanField('Frostsikring tak/takrenner')
    frost_protection_pipe = frost_protection_pipe
    concrete = BooleanField('Betong')


class RoomForm(FlaskForm):
    """Input form for room."""
    room_name = StringField(
        'Rom/stednavn',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            Length(
                min=2,
                max=100,
                message="Navnet bør være mellom %(min)d og %(max)d tegn.")
        ])
    maxEffect = BetterDecimalField()
    normalEffect = BetterDecimalField()
    outside = BooleanField('Utvendig')
    area = BetterDecimalField(
        'Areal',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            NumberRange(min=0.1, max=1000)
        ])
    heated_area = BetterDecimalField(
        'Oppvarmet Areal',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            NumberRange(min=0.1, max=1000)
        ])
    customer_id = HiddenField(validators=[
        DataRequired(
            'Mottok ikke et kunde-objekt. Dette er sansynligvis en feil.')
    ])
    id = HiddenField()
    check_earthed = FormField(CheckEarthed)
    check_max_temp = FormField(CheckMaxTemp)
    check_control_system = FormField(CheckControlSystem)
    curcuit_breaker_size = BetterDecimalField('Sikringsstørrelse')
    ground_fault_protection = BetterDecimalField('Utløserstrøm jordfeil')
    installation_depth = BetterDecimalField('Montasjedybde')
    handed_to_owner = BooleanField('Dokumentasjonen er overlevert')
    owner_informed = BooleanField('Eier og/eller bruker er informert')
    inside_specs = FormField(HeatingInside)
    outside_specs = FormField(HeatingOutside)


class AddressForm(SubForm):
    """Input-form for Adresses."""

    address1 = StringField(
        'Adresse',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=2,
                max=180,
                message="Adressen bør være mellom %(min)d og %(max)d tegn.")
        ])
    address2 = StringField(
        'Adresse 2',
        validators=[
            Length(
                max=180, message="Adresse-linje 2 er for lang (maks 180 tegn).")
        ])
    post_code = IntegerField(
        'Postnummer',
        validators=[
            DataRequired('Feltet er påkrevd'),
            NumberRange(
                min=0, max=9999, message="Postnummeret skal ha 4 siffer.")
        ])
    post_area = StringField(
        'Poststed',
        validators=[DataRequired('Feltet er påkrevd'),
                    Length(min=2, max=180)])


class AddressOptional(SubForm):
    """Optional address."""
    address1 = StringField(
        'Adresse',
        validators=[
            Optional(),
            Length(
                min=2,
                max=180,
                message="Adressen bør være mellom %(min)d og %(max)d tegn.")
        ])
    address2 = StringField(
        'Adresse 2',
        validators=[
            Optional(),
            Length(
                max=180, message="Adresse-linje 2 er for lang (maks 180 tegn).")
        ])
    post_code = IntegerField(
        'Postnummer',
        validators=[
            Optional(),
            NumberRange(
                min=0, max=9999, message="Postnummeret skal ha 4 siffer.")
        ])
    post_area = StringField(
        'Poststed', validators=[Optional(), Length(min=2, max=180)])


class Invite(FlaskForm):
    pass


class CustomerForm(FlaskForm):
    address = FormField(AddressForm)
    address2 = FormField(AddressOptional)

    customer_name = StringField(
        'Navn', validators=[Length(max=100)])
    customer_name2 = StringField(
        'Navn', validators=[Length(max=100)])
    org_nr = IntegerField(
        'Organisasjonsnummer',
        validators=[
            Optional(),
            NumberRange(
                min=100000000,
                max=999999999,
                message='Organisasjonsnummer skal ha totalt 9 siffer.')
        ])
    phone = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    mobile = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    contact_name = StringField(
        'Kontaktperson',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(min=2, message="Minst %(min)d tegn her."),
            Length(max=180, message="Maksimalt %(max)d tegn her.")
        ])
    phone = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    mobile = TelField(
        'Mobil',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    contact_name = StringField(
        'Kontaktperson',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(min=2, message="Minst %(min)d tegn her."),
            Length(max=180, message="Maksimalt %(max)d tegn her.")
        ])
    phone2 = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    mobile2 = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    contact_name2 = StringField(
        'Kontaktperson',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(min=2, message="Minst %(min)d tegn her."),
            Length(max=180, message="Maksimalt %(max)d tegn her.")
        ])
    id = HiddenField()

class Measurement(SubForm):
    """Form for measurements for a HeatingCable."""
    ohm = BetterDecimalField()
    mohm = BetterDecimalField()
    date = DateField(format='%Y-%m-%d')


class MeasurementsForms(SubForm):
    """Form for measurements for a HeatingCable."""
    install = FormField(Measurement)
    pour = FormField(Measurement)
    connect = FormField(Measurement)


class AreaOutput(SubForm):
    v = BetterDecimalField(
        'Flateeffekt <br class="visible-xs-inline" /><span class="text-nowrap">( W/m<sup>2</sup> )</span>'
    )
    m = BooleanField()


class Cc(SubForm):
    v = BetterDecimalField(
        'C/C-avstand <br class="visible-xs-inline" /><span class="text-nowrap">( cm )</span>'
    )
    m = BooleanField()


class InstallationDepth(SubForm):
    v = BetterDecimalField(
        'Montasjedybde <span class="text-nowrap">( mm )</span>')
    m = BooleanField()


class CurcuitBreakerSize(SubForm):
    v = BetterDecimalField('Sikringsstørrelse')
    m = BooleanField()


class SpecsForm(SubForm):
    """Form for combining some different specs for heatingcable."""
    measurements = FormField(MeasurementsForms)
    area_output = FormField(AreaOutput)
    cc = FormField(Cc)
    curcuit_breaker_size = FormField(CurcuitBreakerSize)
    installation_depth = FormField(InstallationDepth)


class HeatingCableForm(FlaskForm):
    """Form for filling in info about a heating-cable."""
    # room_item_id = HiddenField()
    id = HiddenField(validators=[DataRequired()])
    product_id = HiddenField(
        validators=[DataRequired('Vennligst velg en varmekabel.')])
    room_id = HiddenField(validators=[
        DataRequired(
            'Mottok ikke et id for rom. Dette er sansynligvis en feil.')
    ])
    specs = FormField(SpecsForm)


class MultiSave(FlaskForm):
    heating_cables = FieldList(FormField(HeatingCableForm))
    rooms = FieldList(FormField(RoomForm))


class CreateCompany(FlaskForm):
    """Input-form for creating a company."""

    class Meta(AutoAttrMeta):
        pass

    name = StringField(
        'Firma navn',
        validators=[DataRequired('Feltet er påkrevd'),
                    Length(min=2, max=180)])
    description = StringField('Beskrivelse', validators=[Length(max=500)])
    org_nr = IntegerField(
        'Organisasjonsnummer',
        validators=[
            DataRequired('Feltet er påkrevd'),
            NumberRange(
                min=100000000,
                max=999999999,
                message='Organisasjonsnummer skal ha totalt 9 siffer.')
        ])
    phone = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    mobile = TelField(
        'Telefon',
        description='8 siffer. For internasjonale nummer, bruk 00 foran.',
        validators=[
            Regexp(
                '\d{8}|00[-\w]{3,20}',
                message=
                'Telefonnummeret må ha 8 siffer. For internasjonale nummer, bruk 00 foran.'
            )
        ])
    contact_name = StringField(
        'Kontaktperson',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(min=2, message="Minst %(min)d tegn her."),
            Length(max=180, message="Maksimalt %(max)d tegn her.")
        ])
    installer_name = StringField(
        'Innstallatør',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(min=2, message="Minst %(min)d tegn her."),
            Length(max=180, message="Maksimalt %(max)d tegn her.")
        ])
    email = EmailField(
        'Epost',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=6,
                max=70,
                message=("Epost-adressen bør være mellom",
                         "%(min)d og %(max)d tegn."))
        ])
    address = FormField(AddressForm)
    lat = DecimalField(
        DataRequired('Feltet er påkrevd'),
        validators=[NumberRange(min=-85.0000, max=85)])
    lng = DecimalField(
        DataRequired('Feltet er påkrevd'),
        validators=[NumberRange(min=-180.000, max=180)])
