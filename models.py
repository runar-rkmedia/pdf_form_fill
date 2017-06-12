"""Database-structure for item-catalog."""

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import (
    OAuthConsumerMixin,
)
from flask_login import (
    UserMixin,
)
# import bleach
import enum
from field_dicts.helpers import id_generator
db = SQLAlchemy()


class ContactType(enum.Enum):
    """Enumeration for types of contactfields."""
    phone = 1,
    email = 2,
    mobile = 3


def lookup_vk(manufacturor, watt_per_meter, watt_total):
    """Return a specific heating_cable from a generic lookup."""
    products = Product.query\
        .filter_by(effekt=watt_total)\
        .join(ProductType, aliased=True)\
        .filter_by(watt_per_meter=watt_per_meter)\
        .join(ProductType.manufacturor, aliased=True)\
        .filter_by(name=manufacturor)\
        .all()
    return products


class Address(db.Model):
    """Address-table for users."""
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    linje1 = db.Column(db.String(200))
    linje2 = db.Column(db.String(200))
    postnumber = db.Column(db.SmallInteger)
    postal = db.Column(db.String(200))


class Contact(db.Model):
    """Contact-table for users, like phone, email"""
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.Enum(ContactType))
    value = db.Column(db.String(200))


class Company(db.Model):
    """Company-table for users."""
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    orgnumber = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey(Address.id))
    address = db.relationship(
        Address, primaryjoin='Company.address_id==Address.id')


class CompanyContact(db.Model):
    """Associations-table for company and contacts."""
    __tablename__ = 'company_contact'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))


class User(db.Model, UserMixin):
    """User-table for users."""
    __tablename__ = 'vk_user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    given_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    title = db.Column(db.String(50))
    signature = db.Column(db.Binary())
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='User.company_id==Company.id')

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
    __tablename__ = 'invite'

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
            Invite.invitee_user_id == None)

    @classmethod
    def get_invite_from_id(cls, invite_id):
        """Return a valid invite from an id."""
        return Invite.query.filter(
            Invite.id == invite_id,
            Invite.invitee_user_id == None).first()

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
            db.session.add(invite)
            db.session.commit()
        else:
            raise ValueError("Du har nådd din maksgrense for invitasjoner. Når noen har aktivert en av dine invitasjons-lenker og registrert seg, kan du lage nye invitasjons-lenker.") # noqa

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
    __tablename__ = 'user_contact'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    contact = db.relationship(
        Contact, primaryjoin='UserContact.contact_id==Contact.id')
    user = db.relationship(
        User, primaryjoin='UserContact.user_id==User.id')


class Manufacturor(db.Model):
    """Manufacturor-table."""
    __tablename__ = 'manufacturors'
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
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    mainSpec = db.Column(db.String(25))
    watt_per_meter = db.Column(db.Numeric(6))
    watt_per_square_meter = db.Column(db.Numeric(6))
    ledere = db.Column(db.Integer)
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
            'ledere': self.ledere,
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
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    effekt = db.Column(db.Numeric(8))
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
            'effect': self.effekt
        }
        return dictionary


class ProductSpec(db.Model):
    """ProductSpec-table."""
    __tablename__ = 'product_specs'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    key = db.Column(db.String(25))
    value = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(
        Product, primaryjoin='ProductSpec.product_id==Product.id')
