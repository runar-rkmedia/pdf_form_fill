"""Forms used for HTML.."""
# -*- coding: utf-8 -*-
import decimal

from flask_wtf import FlaskForm
from wtforms import (  # RadioField,
    BooleanField,
    FormField,
    HiddenField,
    StringField,
    IntegerField as baseIntegerField
)
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import DecimalField, EmailField, IntegerField
from wtforms.validators import (  # Email,
    DataRequired,
    Length,
    NumberRange,
    ValidationError
)
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
        'Eventuell brtuk av beskyttelsesutstyr',  # noqa
        validators=[Length(max=100)])


class CheckEarthed(SubForm):
    cable_screen = BooleanField('Jordet kabelskjerm')
    chicken_wire = BooleanField('Jordet netting')
    other = StringField('Annet', validators=[Length(max=100)])


class CheckControlSystem(SubForm):
    floor_sensor = BooleanField('Gulvføler'  # noqa
                               )
    room_sensor = BooleanField('Romføler'  # noqa
                              )
    designation = StringField(
        'Typebetegnelse',  # noqa
        validators=[Length(max=50)])
    other = StringField(
        'Annet',  # noqa
        validators=[Length(max=100)])


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


class Invite(FlaskForm):
    pass


class CustomerForm(FlaskForm):
    address = FormField(AddressForm)
    customer_name = StringField('Kundenavn', validators=[Length(max=100)])
    id = HiddenField()


class MeasurementsForms(SubForm):
    """Form for measurements for a HeatingCable."""
    ohm_a = BetterDecimalField()
    ohm_b = BetterDecimalField()
    ohm_c = BetterDecimalField()
    mohm_a = BetterDecimalField()
    mohm_b = BetterDecimalField()
    mohm_c = BetterDecimalField()


class AreaOutput(SubForm):
    v = BetterDecimalField('Flateeffekt ( W/m<sup>2</sup> )')
    m = BooleanField()


class Cc(SubForm):
    v = BetterDecimalField('C/C-avstand ( cm )')
    m = BooleanField()


class SpecsForm(SubForm):
    """Form for combining some different specs for heatingcable."""
    measurements = FormField(MeasurementsForms)
    area_output = FormField(AreaOutput)
    cc = FormField(Cc)


class HeatingCableForm(FlaskForm):
    """Form for filling in info about a heating-cable."""
    room_item_id = HiddenField()
    id = HiddenField()
    product_id = HiddenField(
        validators=[DataRequired('Vennligst velg en varmekabel.')])
    room_id = HiddenField(validators=[
        DataRequired(
            'Mottok ikke et id for rom. Dette er sansynligvis en feil.')
    ])
    specs = FormField(SpecsForm)


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
            NumberRange(
                min=100000000,
                max=999999999,
                message='Organisasjonsnummer skal ha totalt 9 siffer.')
        ])
    contact_name = StringField(
        'Kontaktperson',
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
