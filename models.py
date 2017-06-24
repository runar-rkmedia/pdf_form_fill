"""Database-structure for item-catalog."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_, text
from sqlalchemy.sql.expression import func
from flask_dance.consumer.backend.sqla import (
    OAuthConsumerMixin,
)
from flask_login import (
    UserMixin,
)
# import bleach
import enum
from field_dicts.helpers import id_generator
from datetime import datetime, timedelta
db = SQLAlchemy()

PER_PAGE = 5


class ContactType(enum.Enum):
    """Enumeration for types of contactfields."""
    phone = 1,
    email = 2,
    mobile = 3


def lookup_vk(manufacturor, watt_per_meter, watt_total):
    """Return a specific heating_cable from a generic lookup."""
    products = Product.query\
        .filter_by(effect=watt_total)\
        .join(ProductType, aliased=True)\
        .filter_by(watt_per_meter=watt_per_meter)\
        .join(ProductType.manufacturor, aliased=True)\
        .filter_by(name=manufacturor)\
        .all()
    return products


class Address(db.Model):
    """Address-table for users."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    line1 = db.Column(db.String(200))
    line2 = db.Column(db.String(200))
    postnumber = db.Column(db.SmallInteger)
    postal = db.Column(db.String(200))

    @classmethod
    def update_or_create(cls, address_id, line1, line2, postnumber, postal):
        """Update if exists, else create Address."""
        address = Address.query.filter_by(
            id=address_id
        ).first()
        try:
            postnumber = int(postnumber)
        except TypeError as e:
            raise ValueError(
                'Expected postnumber to be an integer, got {}'
                .format(postnumber))

        if not address:
            address = Address(
                line1=line1,
                line2=line2,
                postnumber=postnumber,
                postal=postal
            )
        else:
            if (
                address.line1 != line1 or
                address.line2 != line2 or
                address.postnumber != postnumber or
                address.postal != postal
            ):
                address.line1 = line1
                address.line2 = line2
                address.postnumber = postnumber
                address.postal = postal
                db.session.add(address)

        return address


class Contact(db.Model):
    """Contact-table for users, like phone, email"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.Enum(ContactType))
    value = db.Column(db.String(200))


class Company(db.Model):
    """Company-table for users."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    orgnumber = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey(Address.id))
    address = db.relationship(
        Address, primaryjoin='Company.address_id==Address.id')

    def get_forms(self, per_page=PER_PAGE, page=1):
        """Return all filled forms created by user."""
        query = FilledForm\
            .query\
            .filter(FilledForm.company==self)\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=True
                )

        modifications = []
        for i in query.items:
            modifications.append(i.modifications[0])

        return modifications, query.pages


class CompanyContact(db.Model):
    """Associations-table for company and contacts."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))


class User(db.Model, UserMixin):
    """User-table for users."""
    __tablename__ = 'vk_users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    given_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    title = db.Column(db.String(50))
    signature = db.Column(db.Binary())
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='User.company_id==Company.id')

    def get_forms(self, per_page=PER_PAGE, page=1):
        """Return all filled forms created by user."""
        subq = db.session\
            .query(
                func.max(FilledFormModified.id)
                )\
            .filter(FilledFormModified.user==self)\
            .group_by(FilledFormModified.filled_form_id)\
            .subquery()
        query = FilledFormModified\
            .query\
            .filter(FilledFormModified.id.in_(subq))\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=True
                )

        return query.items, query.pages

    def addContact(self, contact_type, contact_value):
        """Description."""
        contact = Contact(type=contact_type, value=contact_value)
        db.session.add(contact)
        user_contact = UserContact(
            contact=contact,
            user=self
        )
        db.session.add(user_contact)


class Invite(db.Model):
    """Invite-table for users."""

    id = db.Column(db.String, unique=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='Invite.company_id==Company.id')
    inviter_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    inviter = db.relationship(
        User, primaryjoin='Invite.inviter_user_id==User.id')
    invitee_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    invitee = db.relationship(
        User, primaryjoin='Invite.invitee_user_id==User.id')

    @classmethod
    def get_random_unique_invite_id(cls):
        """Return a random unique id for the invite-table."""
        rand = id_generator()
        while db.session.query(Invite).filter(
                Invite.id == rand).limit(1).first() is not None:
            rand = id_generator()

        return rand

    @classmethod
    def get_invites_from_user(cls, inviter):
        """Return all invites from user which are still valid for signup."""
        return Invite.query.filter(
            Invite.inviter_user_id == inviter.id,
            Invite.invitee_user_id == None)  # noqa

    @classmethod
    def get_invite_from_id(cls, invite_id):
        """Return a valid invite from an id."""
        return Invite.query.filter(
            Invite.id == invite_id,
            Invite.invitee_user_id == None).first()  # noqa

    @classmethod
    def create(cls, inviter):
        """Create a new invite."""
        invites = cls.get_invites_from_user(inviter).count()
        if invites < 10:
            invite = Invite(
                id=cls.get_random_unique_invite_id(),
                company=inviter.company,
                inviter=inviter,
            )
            return invite

        else:
            raise ValueError("Du har nådd din maksgrense for invitasjoner. Når noen har aktivert en av dine invitasjons-lenker og registrert seg, kan du lage nye invitasjons-lenker.")  # noqa

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        dictionary = {
            'url': self.id,
            'company_name': self.company.name,
        }
        return dictionary


class OAuth(db.Model, OAuthConsumerMixin):
    """Oath-table."""
    __tablename__ = 'oauth'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class UserContact(db.Model):
    """Associations-table for user and contacts."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    contact = db.relationship(
        Contact, primaryjoin='UserContact.contact_id==Contact.id')
    user = db.relationship(
        User, primaryjoin='UserContact.user_id==User.id')


class Manufacturor(db.Model):
    """Manufacturor-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        product_types = ProductType.query.filter_by(manufacturor=self).all()
        product_type_dict = [i.serialize for i in product_types]

        dictionary = {
            'id': self.id,
            'name': self.name,
            'product_types': product_type_dict
        }
        return dictionary


class ProductType(db.Model):
    """ProcuctTypes-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    mainSpec = db.Column(db.String(25))  # Betegnelse
    watt_per_meter = db.Column(db.Numeric(6))
    watt_per_square_meter = db.Column(db.Numeric(6))
    secondSpec = db.Column(db.Integer)  # antall ledere
    manufacturor_id = db.Column(db.Integer, db.ForeignKey(Manufacturor.id))
    manufacturor = db.relationship(
        Manufacturor, primaryjoin='ProductType.manufacturor_id==Manufacturor.id')  # noqa

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        products = Product.query.filter_by(product_type=self).all()
        products_dict = [i.serialize for i in products]

        dictionary = {
            'id': self.id,
            'name': self.name,
            'secondSpec': self.secondSpec,
            'products': products_dict
        }
        if self.watt_per_meter:
            dictionary['watt_per_meter'] = self.watt_per_meter
        if self.watt_per_square_meter:
            dictionary[
                'watt_per_square_meter'] = self.watt_per_square_meter
        return dictionary


class Product(db.Model):
    """Product-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    effect = db.Column(db.Numeric(8))
    product_type_id = db.Column(db.Integer, db.ForeignKey(ProductType.id))
    product_type = db.relationship(
        ProductType, primaryjoin='Product.product_type_id==ProductType.id')

    def add_keys_from_dict(self, dictionary):
        """Will create ProducSpecs for this product from a dictionary."""
        for key, val in dictionary.items():
            db.session.add(ProductSpec(key=key, value=val, product=self))

    def get_specs(self):
        """Retrieve all specs for this product."""
        return ProductSpec.query.filter_by(product_id=self.id).all()

    @classmethod
    def get_by_id(cls, p_id):
        """Return object by id."""
        return Product.query.filter_by(id=p_id).first()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        dictionary = {
            'id': self.id,
            'effect': self.effect
        }
        return dictionary


class ProductSpec(db.Model):
    """ProductSpec-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    key = db.Column(db.String(25))
    value = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(
        Product, primaryjoin='ProductSpec.product_id==Product.id')


class FilledForm(db.Model):
    """Table of forms filled by users."""
    __tablename__ = 'filled_form'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))  # e.g. room name
    customer_name = db.Column(db.String(250))
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='FilledForm.company_id==Company.id')
    address_id = db.Column(db.Integer, db.ForeignKey(Address.id))
    address = db.relationship(
        Address, primaryjoin='FilledForm.address_id==Address.id')

    @classmethod
    def update_or_create(
            cls,
            filled_form_id,
            user,
            name,
            customer_name,
            request_form,
            form_data,
            company,
            address):
        """Update if exists, else create FilledForm."""
        filled_form = None
        if filled_form_id:
            filled_form = FilledForm.query.filter(
                FilledForm.id == filled_form_id
            ).first()
        if not filled_form:
            filled_form = FilledForm(
                name=name,
                customer_name=customer_name,
                company=company,
                address=address
            )
        else:
            filled_form.name = name
            filled_form.customer_name = customer_name
            filled_form.company = company
            filled_form.address = address

        db.session.add(filled_form)
        FilledFormModified.update_or_create(
            user=user,
            filled_form=filled_form,
            request_form=request_form,
            form_data=form_data)
        return filled_form

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        mod = self.modifications[0]

        dictionary = {
            'id': self.id,
            'date': mod.date
        }
        dictionary['request_form'] = mod.request_form
        dictionary['address_id'] = self.address.id
        return dictionary




class FilledFormModified(db.Model):
    """Table of modification-dated for FilledForm-model."""
    __tablename__ = 'filled_form_modified'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(
        User, primaryjoin='FilledFormModified.user_id==User.id')
    filled_form_id = db.Column(db.Integer, db.ForeignKey(FilledForm.id))
    filled_form = db.relationship(
        FilledForm,
        primaryjoin='FilledFormModified.filled_form_id==FilledForm.id',
        backref='modifications')  # noqa
    date = db.Column(db.DateTime, default=datetime.utcnow)
    request_form = db.Column(db.JSON)  # All data from the users-form
    form_data = db.Column(db.JSON)  # All data actually used to fill the pdf.
    info = {'bind_key': 'forms'}

    __mapper_args__ = {
        "order_by":date.desc()
    }

    @classmethod
    def update_or_create(cls, user, filled_form, request_form, form_data):
        """
        Create modification-date if last update was either not made by
        current user, or within the last 5 minutes."""
        if not user:
            ValueError('Expected a user, got {}'.format(user))
        if not filled_form:
            ValueError('Expected a filled_form, got {}'.format(filled_form))
        last_modified = None
        if user.id:
            last_modified = FilledFormModified.query.filter(
                FilledFormModified.filled_form == filled_form).order_by(
                    desc(FilledFormModified.date)).filter(
                        or_(
                            FilledFormModified.user != user,
                            FilledFormModified.date >= (
                                datetime.utcnow() - timedelta(seconds=1))
                        )).first()
        if not last_modified:
            last_modified = FilledFormModified(
                user=user,
                filled_form=filled_form
            )
        last_modified.request_form = request_form
        last_modified.form_data = form_data
        db.session.add(last_modified)
        return last_modified

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        creation_time = db.session\
            .query(
                FilledFormModified.date
            )\
            .filter(
                FilledFormModified.filled_form_id == self.filled_form_id)\
            .order_by(FilledFormModified.date)\
            .first()

        dictionary = {
            'id': self.id,
            'date': self.date
        }
        if creation_time:
            dictionary['creation_time'] = creation_time
        if self.filled_form:
            dictionary['request_form'] = self.request_form
            dictionary['address_id'] = self.filled_form.address.id
        return dictionary
