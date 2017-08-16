from enum import Enum
from models import db, ByID


class ProductCatagory(Enum):
    """Enumeration for catagories of products."""
    cable_inside = 1,
    cable_outside = 2,
    mat_inside = 3
    mat_outside = 4
    single_inside = 5
    single_outside = 6

    @classmethod
    def split(cls, enumObject):
        """Split it."""
        catagory_type = ''
        if enumObject in [cls.cable_inside, cls.cable_outside]:
            catagory_type = 'cable'
        elif enumObject in [cls.mat_inside, cls.mat_outside]:
            catagory_type = 'mat'
        elif enumObject in [cls.single_inside, cls.single_outside]:
            catagory_type = 'single'
        return catagory_type, enumObject in [
            cls.cable_outside, cls.mat_outside, cls.single_outside
        ]


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
    manufacturor_id = db.Column(db.Integer, db.ForeignKey(Manufacturor.id))
    manufacturor = db.relationship(
        Manufacturor, primaryjoin='ProductType.manufacturor_id==Manufacturor.id')  # noqa
    mainSpec = db.Column(db.SmallInteger)  # electrical effect per meter(squared)
    secondarySpec = db.Column(db.SmallInteger)
    catagory = db.Column(db.Enum(ProductCatagory))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        products = Product.query.filter_by(product_type=self).all()
        products_dict = [i.serialize for i in products]

        dictionary = {
            'id': self.id,
            'name': self.name,
            'mainSpec': self.mainSpec,
            'secondarySpec': self.secondarySpec,
            'products': products_dict
        }
        dictionary['type'], dictionary[
            'inside'] = ProductCatagory.split(self.catagory)
        return dictionary


class Product(db.Model, ByID):
    """Product-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    effect = db.Column(db.Numeric(8))
    product_type_id = db.Column(db.Integer, db.ForeignKey(ProductType.id))
    product_type = db.relationship(
        ProductType, primaryjoin='Product.product_type_id==ProductType.id')
    specs = db.Column(db.JSON)
    restrictions = db.Column(db.JSON)

    @classmethod
    def get_by_id(cls, p_id):
        """Return object by id."""
        return Product.query.filter_by(id=p_id).first()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        dictionary = {
            'id': self.id,
            'effect': self.effect,
            'restrictions': self.restrictions
        }
        return dictionary
