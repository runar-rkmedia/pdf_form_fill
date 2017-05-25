"""Database-structure for item-catalog."""

from flask_sqlalchemy import SQLAlchemy
import bleach
db = SQLAlchemy()


def lookup_vk(manufacturor, watt_per_meter, watt_total):
    """Return a specific heating_cable from a generic lookup."""
    products = Product.query\
        .filter_by(effekt=watt_total)\
        .join(ProductType, aliased=True)\
        .filter_by(watt_per_meter=watt_per_meter)\
        .join(ProductType.manufacturor, aliased=True)\
        .filter_by(name=manufacturor)\
        .all()
    for p in products:
        print(p.name)
    return products


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
