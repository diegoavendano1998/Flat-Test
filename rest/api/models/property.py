from api import db

from datetime import datetime

class Property (db.Model):
    __tablename__ = 'products'
    id          = db.Column (db.Integer, primary_key=True)
    name        = db.Column (db.String(200))
    description = db.Column (db.Text)
    price       = db.Column (db.Float)
    surface     = db.Column (db.Float)
    category_id = db.Column (db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created     = db.Column (db.DateTime(timezone=False), nullable=False, default=datetime.utcnow())
    deleted     = db.Column (db.Integer,default=0)

    def __init__(self, name, description, price, surface, category_id, deleted=0):
        self.name           = name
        self.description    = description
        self.price          = price
        self.surface        = surface
        self.category_id    = category_id
        self.deleted        = deleted

    # '[<Product 'producto1'>, <Product 'producto2'>]'
    def __repr__(self):
        return '<Product %r>' %(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'price': self.price,
            'name': self.name 
        }