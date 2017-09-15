"""User-tables for pdf_form_fill."""

from datetime import datetime, timedelta

from enum import Enum
from sqlalchemy import desc, exc, or_
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func

import my_exceptions
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from models import PER_PAGE, ByID, MyBaseModel, NoAccess, db
from models_product import Product
from pdf_filler.helpers import id_generator


class ContactType(Enum):
    """Enumeration for types of contactfields."""
    phone = 1,
    email = 2,
    mobile = 3


class InviteType(Enum):
    """Enumeration for types of invites."""
    company = 1,
    create_company = 2,


class UserRole(Enum):
    """Enumeration for types of user-roles."""
    user = 1,
    companyAdmin = 2,
    admin = 3


class RoomTypeInfo(ByID, db.Model):
    """Table for room-info."""
    normalEffect = db.Column(db.SmallInteger(), nullable=False)
    maxEffect = db.Column(db.SmallInteger(), nullable=False)
    names = db.Column(postgresql.ARRAY(db.String(), dimensions=1))
    outside = db.Column(db.Boolean(), default=False)

    @property
    def serialize(self):
        """Return stuff."""
        d = {
            'id': self.id,
            'normalEffect': self.normalEffect,
            'maxEffect': self.maxEffect,
            'names': self.names,
        }
        if self.outside:
            d['outside'] = self.outside
        return d


class Address(MyBaseModel, db.Model):
    """Address-table for users."""
    address1 = db.Column(db.String(200), nullable=False)
    address2 = db.Column(db.String(200))
    post_code = db.Column(db.SmallInteger, nullable=False)
    post_area = db.Column(db.String(200), nullable=False)

    @classmethod
    def update_or_create(
            cls, address_id, address1, address2, post_area, post_code):
        """Update if exists, else create Address."""
        address = Address.query.filter_by(
            id=address_id
        ).first()

        if not address:
            address = Address()
        address.address1 = address1
        address.address2 = address2
        address.post_code = post_code
        address.post_area = post_area
        db.session.add(address)

        return address

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        dictionary = {
            'address1': self.address1,
            'address2': self.address2,
            'post_code': self.post_code,
            'post_area': self.post_area
        }
        return dictionary


class Contact(ByID, db.Model):
    """Contact-table for users, like phone, email"""
    type = db.Column(db.Enum(ContactType))
    value = db.Column(db.String(200))
    description = db.Column(db.String(200))


class Company(MyBaseModel, db.Model):
    """Company-table for users."""

    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    description = db.Column(db.String(500))
    orgnumber = db.Column(db.Integer,
                          unique=True,
                          nullable=False)
    address_id = db.Column(
        db.Integer,
        db.ForeignKey(Address.id),
        nullable=False)
    address = db.relationship(
        Address,
        primaryjoin='Company.address_id==Address.id')
    lat = db.Column(db.Numeric(8, 6))
    lng = db.Column(db.Numeric(9, 6))

    def add_contact(self, c_type, value, description):
        """Add contact to this company."""
        contact = Contact(
            type=c_type,
            value=value,
            description=description
        )
        company_contact = CompanyContact(
            contact=contact,
            company=self
        )
        db.session.add(contact)
        db.session.add(company_contact)
        return contact

    def owns(self, model):
        """Check if company has rights to access this."""
        if model.company == self:
            return True
        else:
            raise my_exceptions.NotAuthorized()

    @classmethod
    def customer_list_query(cls, company_id):
        """Return a query with all the customers at a company."""
        return Customer.query.\
            filter(
                (
                    (Customer.company_id == company_id)
                    & (Customer.archived != True)
                )
            )\


    @classmethod
    def update_or_create(
            cls, company_id, name, description, orgnumber, address, lat, lng):
        """Update if exists, else create Company."""
        if not isinstance(address, Address):
            raise ValueError(
                "Did not recieve an Address-type, got '{}'".format(address))
        company = Company.query.filter_by(
            id=company_id
        ).first()

        if not company:
            company = Company()
        company.name = name
        company.description = description
        company.orgnumber = orgnumber
        company.address = address
        company.lat = lat
        company.lng = lng
        try:
            db.session.add(company)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            raise my_exceptions.DuplicateCompany()
        else:
            pass

        return company

    @classmethod
    def update_or_create_all(cls, form, company=None):
        """up."""
        if company:
            company_id = company.id
        else:
            company_id = None
        if company and company.address:
            address_id = company.address.id
        else:
            address_id = None
        address = Address.update_or_create(
            address_id=address_id,
            address1=form.address.address1.data,
            address2=form.address.address2.data,
            post_area=form.address.post_area.data,
            post_code=form.address.post_code.data,
        )

        company = Company.update_or_create(
            company_id=company_id,
            name=form.name.data,
            description=form.description.data,
            orgnumber=form.org_nr.data,
            address=address,
            lat=form.lat.data,
            lng=form.lng.data
        )
        if company.contacts:
            company.contacts[0].contact.value = form.email.data
            company.contacts[0].contact.description = form.contact_name.data
            db.session.add(company.contacts[0])
        else:
            company.add_contact(
                c_type=ContactType.email,
                value=form.email.data,
                description=form.contact_name.data
            )
        return company


class CompanyContact(ByID, db.Model):
    """Associations-table for company and contacts."""
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    contact = db.relationship(
        Contact, primaryjoin='CompanyContact.contact_id==Contact.id')
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='CompanyContact.company_id==Company.id',
        backref='contacts')


class User(ByID, UserMixin, db.Model):
    """User-table for users."""
    __tablename__ = 'vk_users'
    given_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    title = db.Column(db.String(50))
    role = db.Column(db.Enum(UserRole), default='user')
    signature = db.Column(db.Binary())
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='User.company_id==Company.id')
    last_modified_customer_id = db.Column(
        db.Integer, db.ForeignKey('customer.id'))
    last_modified_customer = db.relationship(
        'Customer', primaryjoin='User.last_modified_customer_id==Customer.id', post_update=True)

    @property
    def last_edit(self):
        """Return the last edit the user made to a customer."""
        if not self.last_modified_customer:
            return None
        if (
            self.last_modified_customer.owns(self) and
                not self.last_modified_customer.archived):
            return self.last_modified_customer

    def get_forms(self, per_page=PER_PAGE, page=1):
        """Return all filled forms created by user."""
        return [], 0
        subq = db.session\
            .query(
                func.max(RoomItem.id)
            )\
            .filter(
                (RoomItem.user == self) &
                (RoomItem.archived != True)  # noqa
            )\
            .group_by(RoomItem.room_id)\
            .subquery()
        query = RoomItem\
            .query\
            .filter(RoomItem.id.in_(subq))\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=True
            )

        filled_forms = []
        for mod in query.items:
            if mod.room and not mod.room.archived:
                filled_forms.append(mod.room)

        return filled_forms, query.pages

    def owns(self, model):
        """Check if user has rights to access this."""
        if model.user == self:
            return True
        else:
            raise NoAccess("You don't have access to this resource.")

    def add_contact(self, c_type, value, description):
        """Add contact to this user."""
        contact = Contact(
            type=c_type,
            value=value,
            description=description
        )
        company_contact = UserContact(
            contact=contact,
            user=self
        )
        db.session.add(contact)
        db.session.add(company_contact)
        return contact


class Invite(db.Model):
    """Invite-table for users."""

    id = db.Column(db.String, unique=True, primary_key=True)
    type = db.Column(db.Enum(InviteType), default='company')
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(Company.id)
    )
    company = db.relationship(
        Company, primaryjoin='Invite.company_id==Company.id')
    inviter_user_id = db.Column(
        db.Integer, db.ForeignKey(User.id), nullable=False)
    inviter = db.relationship(
        User,
        primaryjoin='Invite.inviter_user_id==User.id')
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


class OAuth(OAuthConsumerMixin, db.Model):
    """Oath-table."""
    __tablename__ = 'oauth'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class UserContact(ByID, db.Model):
    """Associations-table for user and contacts."""
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    contact = db.relationship(
        Contact, primaryjoin='UserContact.contact_id==Contact.id')
    user = db.relationship(
        User, primaryjoin='UserContact.user_id==User.id')


class Customer(MyBaseModel, db.Model):
    """Customer-table."""
    name = db.Column(db.String(100))
    address_id = db.Column(db.Integer,
                           db.ForeignKey(Address.id),
                           nullable=False)
    address = db.relationship(
        Address, primaryjoin='Customer.address_id==Address.id')
    company_id = db.Column(
        db.Integer, db.ForeignKey(Company.id), nullable=False)
    company = db.relationship(
        Company, primaryjoin='Customer.company_id==Company.id', backref='customers')
    created_by_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_by_user = db.relationship(
        User, primaryjoin='Customer.created_by_user_id==User.id')
    modified_by_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    modified_by_user = db.relationship(
        User, primaryjoin='Customer.modified_by_user_id==User.id')
    date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on_date = db.Column(db.DateTime, default=datetime.utcnow)

    def owns(self, user):
        """Check that user has rights to this customer."""
        if not user.company:
            raise my_exceptions.UserHasNoCompany()
        return user.company.owns(self)

    @classmethod
    def update_or_create(cls, customer, customer_form, user):
        if customer:
            customer.owns(user)
        if not customer:
            address = Address()
            customer = Customer()
            customer.address = address
            customer.company = user.company
            customer.created_by_user = user
            db.session.add(address)
            db.session.add(customer)
        if not customer:
            raise my_exceptions.NotACustomer
        customer.address.update_entity({
            'address1': customer_form.address.address1.data,
            'address2': customer_form.address.address2.data,
            'post_code': customer_form.address.post_code.data,
            'post_area': customer_form.address.post_area.data,
        })
        customer.name = customer_form.customer_name.data
        customer.modified_by_user = user
        customer.modified_on_date = datetime.utcnow()
        user.last_modified_customer = customer
        db.session.commit()
        return customer

    @property
    def serialize(self):
        return {
            'name': self.name,
            'address': self.address.serialize,
            'rooms': [i.serialize for i in self.rooms if not i.archived],
            'id': self.id
        }

    @property
    def serialize_short(self):
        """Serialize for lists of customer."""
        dictionary = {
            'name': self.name,
            'address': self.address.serialize,
            'id': self.id,
            'created': {
                'given_name': self.created_by_user.given_name,
                'family_name': self.created_by_user.family_name,
                'date': self.date
            },
        }
        if (self.date-self.modified_on_date).seconds:
            dictionary['modified'] = {
                'given_name': self.created_by_user.given_name,
                'family_name': self.created_by_user.family_name,
                'date': self.date
            }
        if self.rooms:
            dictionary['rooms'] = [i.name for i in self.rooms if i.archived != True]
        return dictionary


class Room(MyBaseModel, db.Model):
    """Table of forms filled by users."""
    # __tablename__ = 'room'
    name = db.Column(db.String(50))  # e.g. room name
    archived = db.Column(db.Boolean, default=False)
    outside = db.Column(db.Boolean, default=False)
    area = db.Column(db.Numeric(8, 3))
    heated_area = db.Column(db.Numeric(8, 3))
    maxEffect = db.Column(db.Numeric(8, 3))
    normalEffect = db.Column(db.Numeric(8, 3))
    earthed_cable_screen = db.Column(db.Boolean, default=False)
    earthed_chicken_wire = db.Column(db.Boolean, default=False)
    earthed_other = db.Column(db.String(200))
    max_temp_planning = db.Column(db.Boolean, default=False)
    max_temp_installation = db.Column(db.Boolean, default=False)
    max_temp_other = db.Column(db.String(200))
    control_system_floor_sensor = db.Column(db.Boolean, default=False)
    control_system_room_sensor = db.Column(db.Boolean, default=False)
    control_system_designation = db.Column(db.String(200))
    control_system_other = db.Column(db.String(200))

    customer_id = db.Column(
        db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer = db.relationship(
        Customer,
        primaryjoin='Room.customer_id==Customer.id',
        backref='rooms')

    def owns(self, user):
        """Check that user has rights to this room."""
        return self.customer.owns(user)

    @property
    def serialize(self, user=None):
        """Return object data in easily serializeable format"""

        dictionary = {
            'id': self.id,
            'room_name': self.name,
            'heating_cables': [
                i.serialize for i in self.items if not i.archived
            ],
            'outside': self.outside,
            'area': float(self.area or 0),
            'heated_area': float(self.heated_area or 0),
            'maxEffect': float(self.maxEffect or 0),
            'normalEffect': float(self.normalEffect or 0),
            'check_earthed': {
                'cable_screen': self.earthed_cable_screen,
                'chicken_wire': self.earthed_chicken_wire,
                'other': self.earthed_other,
            },
            'check_max_temp': {
                'planning': self.max_temp_planning,
                'installation': self.max_temp_installation,
                'other': self.max_temp_other,
            },
            'check_control_system': {
                'floor_sensor': self.control_system_floor_sensor,
                'room_sensor': self.control_system_room_sensor,
                'designation': self.control_system_designation,
                'other': self.control_system_other,
            }

        }
        return dictionary


class RoomItem(MyBaseModel, db.Model):
    """Holder for modifications to items."""
    room_id = db.Column(
        db.Integer, db.ForeignKey(Room.id), nullable=False)
    room = db.relationship(
        Room,
        primaryjoin='RoomItem.room_id==Room.id',
        backref='items')  # noqa
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def owns(self, user):
        """Check that user has rights to this room-item."""
        return self.room.owns(user)

    @property
    def serialize(self, user=None):
        """Return object data in easily serializeable format"""
        if self.modifications:
            dictionary = self.modifications[0].serialize
            # specs = dictionary.pop('specs')
            # measurements = {}
            dictionary['id'] = self.id
            # dictionary['product_id'] = specs.pop('product_id', None)
            # dictionary['specs'] = specs
            return dictionary

    @property
    def latest(self):
        """Return the latest modification made to this item, by date"""
        if self.modifications:
            return self.modifications[0]

    @property
    def modification_date(self):
        """Return the time of last modification"""
        if self.latest:
            return self.latest.date

    @classmethod
    def update_or_create(
            cls, user, room, product_id, id=None,
            room_item=None, specs={}, pdf_specs={}):
        """Update or create a RoomItemModifications.."""
        if not room_item:
            room_item = RoomItem.by_id(id, user)
        if not room_item:
            room_item = RoomItem(
                room=room
            )
        db.session.add(room_item)
        RoomItemModifications.update_or_create(
            user=user,
            product_id=product_id,
            room_item=room_item,
            specs=specs,
            pdf_specs=pdf_specs
        )
        return room_item


class RoomItemModifications(MyBaseModel, db.Model):
    """Table of modification-dated for Room-model."""
    __tablename__ = 'room_item_modifications'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User, primaryjoin='RoomItemModifications.user_id==User.id')
    archived = db.Column(db.Boolean, default=False)
    room_item_id = db.Column(
        db.Integer, db.ForeignKey(RoomItem.id), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    room_item = db.relationship(
        RoomItem,
        primaryjoin='RoomItemModifications.room_item_id==RoomItem.id',
        backref='modifications')  # noqa
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # All data from the users-form
    specs = db.Column(db.JSON, nullable=True)
    # All data actually used to fill the pdf.
    pdf_specs = db.Column(db.JSON, nullable=True)

    __mapper_args__ = {
        "order_by": date.desc()
    }

    @classmethod
    def update_or_create(cls, user, room_item, specs, product_id, pdf_specs):
        """
        Create modification-date if last update was either not made by
        current user, or within the last 5 minutes."""
        if not user:
            ValueError('Expected a user, got {}'.format(user))
        if not room_item:
            ValueError('Expected a room_item, got {}'.format(room_item))
        last_modified = None
        if user.id:
            last_modified = RoomItemModifications.query.filter(
                RoomItemModifications.room_item == room_item).order_by(
                    desc(RoomItemModifications.date)).filter(
                        or_(
                            RoomItemModifications.user != user,
                            RoomItemModifications.date >= (
                                datetime.utcnow() - timedelta(seconds=60 * 5))
                        )).first()
        if not last_modified:
            last_modified = RoomItemModifications(
                user=user,
                room_item=room_item
            )
        last_modified.specs = specs
        last_modified.product_id = product_id
        db.session.add(last_modified)
        return last_modified

    @property
    def product(self):
        """Return product from stored on this object."""
        return Product.by_id(self.product_id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        creation_time = db.session\
            .query(
                RoomItemModifications.date
            )\
            .filter(
                RoomItemModifications.room_item_id == self.room_item_id)\
            .order_by(RoomItemModifications.date)\
            .first()

        dictionary = {
            'id': self.id,
            'm_date': self.date,
        }
        specs = self.specs.copy()
        dictionary['product_id'] = self.product_id
        if creation_time:
            dictionary['c_date'] = creation_time
        if self.room_item:
            dictionary['specs'] = specs
        return dictionary
