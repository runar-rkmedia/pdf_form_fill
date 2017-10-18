from enum import Enum
from models import db, ByID


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
    # electrical effect per meter(squared)
    mainSpec = db.Column(db.SmallInteger)
    secondarySpec = db.Column(db.SmallInteger)
    isMat = db.Column(db.Boolean, default=False)
    self_limiting = db.Column(db.Boolean, default=False)
    per_meter = db.Column(db.Boolean, default=False)
    inside = db.Column(db.Boolean, default=False)
    outside = db.Column(db.Boolean, default=False)

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
            'products': products_dict,
            'isMat': self.isMat,
            'per_meter': self.per_meter,
            'self_limiting': self.self_limiting,
            'inside': self.inside,
            'outside': self.outside,
        }
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
            'restrictions': {
                'max': self.resistance_max,
                'nom': self.resistance_nominal,
                'min': self.resistance_min
            },
            'specs': self.specs
        }

        return dictionary

    def calculate_nominal_resistance(self):
        if self.effect:
            return float(
                self.product_type.secondarySpec) ** 2 / float(self.effect)
        return 0

    @property
    def resistance_min(self):
        return (self.restrictions.get('R_min') or
                self.calculate_nominal_resistance() / 1.05)

    @property
    def resistance_nominal(self):
        l = (self.restrictions.get('R_nom') or
                self.calculate_nominal_resistance())
        return (self.restrictions.get('R_nom') or
                self.calculate_nominal_resistance())

    @property
    def resistance_max(self):
        return (self.restrictions.get('R_max') or
                self.calculate_nominal_resistance() * 1.10)
