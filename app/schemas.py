from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_enum import EnumField
from sqlalchemy.types import Enum
import models_product as prod
import models_credentials as cred


class ManufacturorSchema(ModelSchema):

    class Meta:
        model = prod.Manufacturor


class ProductTypeSchema(ModelSchema):

    manufacturor = fields.Nested(ManufacturorSchema, exclude=('id',))

    class Meta:
        model = prod.ProductType


class ProductSchema(ModelSchema):

    product_type = fields.Nested(ProductTypeSchema, exclude=('id',))

    class Meta:
        model = prod.Product


class AddressSchema(ModelSchema):

    class Meta:
        model = cred.Address


class ContactSchema(ModelSchema):
    type = EnumField(cred.ContactType, by_value=True)

    class Meta:
        model = cred.Contact


# class ContactTypeSchema(ModelSchema):
#
#
#
#     class Meta:
#         model = cred.ContactType


class CompanyContactSchema(ModelSchema):

    contact = fields.Nested(ContactSchema, only=(
        'description',
        'type',
        'value'
    ))

    class Meta:
        model = cred.CompanyContact


class UserSchema(ModelSchema):

    address = fields.Nested(AddressSchema, only=(
        'address1', 'address2', 'post_code', 'post_code', 'post_area'))

    class Meta:
        model = cred.User


class InviteSchema(ModelSchema):

    class Meta:
        model = cred.Invite


class CompanyScheme(ModelSchema):

    address = fields.Nested(AddressSchema, only=(
        'address1', 'address2', 'post_code', 'post_code', 'post_area'))
    contacts = fields.Nested(
        CompanyContactSchema,
        many=True,
        only='contact')

    class Meta:
        model = cred.Company


class CustomerSchema(ModelSchema):

    address = fields.Nested(AddressSchema, only=(
        'address1', 'address2', 'post_code', 'post_code', 'post_area'))
    company = fields.Nested(CompanyScheme)

    class Meta:
        model = cred.Customer


class RoomSchema(ModelSchema):

    class Meta:
        model = cred.Room


class RoomItemSchema(ModelSchema):

    class Meta:
        model = cred.RoomItem


class RoomItemModificationsSchema(ModelSchema):

    user = fields.Nested(UserSchema)
    product = fields.Function(lambda obj: prod.Product.by_id(obj))
    product = fields.Method('get_this_product')

    def get_this_product(self, obj):
        """Return and serialize this prodocut."""
        product = prod.Product.by_id(obj.product_id)
        if product:
            return ProductSchema(
                # only=('date', 'specs', 'product')
                )\
                .dump(product).data

    class Meta:
        model = cred.RoomItemModifications


product = ProductSchema(exclude=('product_type_id'))
product_type = ProductTypeSchema(exclude=('archived'))
manufacturor = ManufacturorSchema(exclude=('archived'))
address = AddressSchema(exclude=('archived'))
contact = ContactSchema(exclude=(''))
user = UserSchema(only=('id', 'given_name', 'family_name',
                        'email', 'title', 'role', 'company_id'))
invite = InviteSchema(exclude=(''))
customer = CustomerSchema(exclude=('archived'))
room = RoomSchema(exclude=('sign'))
room_item = RoomItemSchema(exclude=('archived'))
room_item_modifications = RoomItemModificationsSchema(exclude=())


def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def room_item_modification_recurcively(entity):
    """Return all info from this and parents."""
    # Be careful with private information leaking here.
    mod_data = RoomItemModificationsSchema(
        only=('date', 'specs', 'product'))\
        .dump(entity).data
    user_data = UserSchema(
        only=('family_name', 'given_name', 'email'))\
        .dump(entity.user).data
    room_data = RoomSchema(
        only=('name', 'specs'))\
        .dump(entity.room_item.room).data
    customer_data = CustomerSchema(
        only=(
            'name',
            'address',
            'company.address',
            'company.contacts',
            'company.description',
            'company.name',
            'company.orgnumber',
        ))\
        .dump(entity.room_item.room.customer).data

    data = {
        'customer': customer_data,
        'room_item_modifications': mod_data,
        'user': user_data,
        'room': room_data,
    }

    # from pprint import pprint
    # pprint(data)
    # pprint(flatten_dict(data))
    return data
