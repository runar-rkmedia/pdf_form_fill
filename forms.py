"""Forms used for HTML.."""
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FormField,
    BooleanField,
    # RadioField,
    HiddenField
)
from wtforms.fields.html5 import EmailField, IntegerField, DecimalField
from wtforms_html5 import AutoAttrMeta
from wtforms.validators import (DataRequired,
                                # Email,
                                Length,
                                NumberRange,
                                ValidationError)


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


class RoomForm(FlaskForm):
    """Input form for room."""
    room_name = StringField(
        'Rom/stednavn',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            Length(
                min=2,
                max=100,
                message="Navnet bør være mellom %(min)d og %(max)d tegn."
            )
        ]
    )
    outside = BooleanField(
        'Utvendig'
    )
    area = DecimalField(
        'Areal',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            NumberRange(
                min=0.1,
                max=1000
            )
        ]
    )
    heated_area = DecimalField(
        'Oppvarmet Areal',
        validators=[
            DataRequired('Feltet er påkrevd.'),
            NumberRange(
                min=0.1,
                max=1000
            )
        ]
    )
    customer_id = HiddenField(
        validators=[
            DataRequired(
                'Mottok ikke et kunde-objekt. Dette er sansynligvis en feil.')
        ]
    )
    id = HiddenField()


class SubForm(FlaskForm):
    """CsrfToken-basic."""

    def __init__(self, **_kwargs):
        _kwargs['csrf_enabled'] = False
        super().__init__(**_kwargs)


class AddressForm(SubForm):
    """Input-form for Adresses."""

    address1 = StringField(
        'Adresse',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=2,
                max=180,
                message="Adressen bør være mellom %(min)d og %(max)d tegn."

            )
        ]
    )
    address2 = StringField(
        'Adresse 2',
        validators=[
            Length(max=180,
                   message="Adresse-linje 2 er for lang (maks 180 tegn)."
                   )
        ]
    )
    post_code = IntegerField(
        'Postnummer',
        validators=[
            DataRequired('Feltet er påkrevd'),
            NumberRange(
                min=0,
                max=9999,
                message="Postnummeret skal ha 4 siffer."
            )
        ]
    )
    post_area = StringField(
        'Poststed',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=2,
                max=180
            )
        ]
    )


class CustomerForm(FlaskForm):
    address = FormField(AddressForm)
    customer_name = StringField(
        'Kundenavn',
        validators=[
            Length(max=100)
        ]
    )
    id = HiddenField()


class MeasurementsForms(SubForm):
    """Form for measurements for a HeatingCable."""
    ohm_a = DecimalField()
    ohm_b = DecimalField()
    ohm_c = DecimalField()
    mohm_a = DecimalField()
    mohm_b = DecimalField()
    mohm_c = DecimalField()


class CalculationsForm(SubForm):
    """Form for calculated values, with override by user."""
    cc = DecimalField(
        'C/C-avstand'
    )
    w_per_m2 = DecimalField(
        'Flateeffect (W/m2)'
    )


class SpecsForm(SubForm):
    """Form for combining some different specs for heatingcable."""
    measurements = FormField(MeasurementsForms)
    calculations = FormField(CalculationsForm)


class HeatingCableForm(FlaskForm):
    """Form for filling in info about a heating-cable."""
    room_item_id = HiddenField()
    id = HiddenField()
    product_id = HiddenField(
        validators=[
            DataRequired(
                'Vennligst velg en varmekabel.')
        ]
    )
    room_id = HiddenField(
        validators=[
            DataRequired(
                'Mottok ikke et id for rom. Dette er sansynligvis en feil.')
        ]
    )
    specs = FormField(SpecsForm)


class HeatingForm(FlaskForm):
    """Form for filling out a heaating-cable."""
    address = FormField(AddressForm)
    room = FormField(RoomForm)


class CreateCompany(FlaskForm):
    """Input-form for creating a company."""

    class Meta(AutoAttrMeta):
        pass

    name = StringField('Firma navn',
                       validators=[DataRequired('Feltet er påkrevd'),
                                   Length(min=2,
                                          max=180)])
    description = StringField('Beskrivelse',
                              validators=[Length(max=500)])
    org_nr = IntegerField(
        'Organisasjonsnummer',
        validators=[
            NumberRange(
                min=100000000,
                max=999999999,
                message='Organisasjonsnummer skal ha totalt 9 siffer.')
        ]
    )
    contact_name = StringField(
        'Kontaktperson',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=2,
                message="Minst %(min)d tegn her."
            ),
            Length(
                max=180,
                message="Maksimalt %(max)d tegn her."
            )
        ]
    )
    email = EmailField(
        'Epost',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=6,
                max=70,
                message=("Epost-adressen bør være mellom",
                         "%(min)d og %(max)d tegn.")
            )
        ]
    )
    address = FormField(AddressForm)
