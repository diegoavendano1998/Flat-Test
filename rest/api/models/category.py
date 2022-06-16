from api import db

class Category (db.Model):
    __tablename__ = 'categories'
    id              = db.Column (db.Integer, primary_key=True)
    name            = db.Column (db.String(200))
    description     = db.Column (db.String(200))
    deleted         = db.Column (db.Integer,default=0)
    products        = db.relationship('Property', backref='category', lazy='select')

    def __init__(self, name, description, deleted=0):
        self.name        = name
        self.description = description
        self.deleted     = 0

    def __repr__(self):
        return '<Category %r>' %(self.name)