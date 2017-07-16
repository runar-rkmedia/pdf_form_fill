from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms_html5 import AutoAttrMeta
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, Regexp

from models import (
    Company
)


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


class AddressForm(FlaskForm):
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
    postnumber = IntegerField(
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
    postal = StringField(
        'Poststed',
        validators=[
            DataRequired('Feltet er påkrevd'),
            Length(
                min=2,
                max=180
            )
        ]
    )



class CreateCompany(FlaskForm):

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
                message="Epost-adressen bør være mellom %(min)d og %(max)d tegn."
            )
        ]
    )
    address = FormField(AddressForm)
