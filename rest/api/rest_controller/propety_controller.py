from flask.views import MethodView
from flask import request, abort

from api.models.property import Property
from api.helpers.request import responseJSON
from api import app, db

import os


class PropertyAPI(MethodView):
    # Find all properties
    def get(self,id=None):
        if id:
            property = Property.query.get(id)
            if not property:
                return responseJSON(None,"Parametros invalidos (id)",403)
            else:
                res = propertyToJSON(property)
        else:
            properties = Property.query.all()
            res=[]
            for p in properties:
                res.append(propertyToJSON(p))
        return responseJSON(res,None,200)

    # Delete a property
    def delete(self, id):
        if id:
            property = Property.query.get(id)
            if not property:
                return responseJSON(None,"Parametros invalidos (id)",403)
            db.session.delete(property)
            db.session.commit()
            return responseJSON("Propiedad eliminada",None,200)
        return responseJSON(None,"Id invalido",403)

    # Add property
    def post(self):
        # NAME
        if not request.form:
            return responseJSON(None,"Sin parametros (name)",403)
        if not "name" in request.form:
            return responseJSON(None,"Parametros invalidos (name)",403)
        # Check for name not null
        if len(request.form['name']) < 1:
            return responseJSON(None,"Nombre invalido",403)
        # DESCRIPTION
        if not "description" in request.form:
            return responseJSON(None,"Parametros invalidos (description)",403)
        if len(request.form['description']) < 1:
            return responseJSON(None,"Descripcción invalida",403)
        # SURFACE
        if not "surface" in request.form:
            return responseJSON(None,"Parametros invalidos (surface)",403)
        if len(request.form['surface']) < 1:
            return responseJSON(None,"Marca invalida",403)   
        # PRICE
        if not "price" in request.form:
            return responseJSON(None,"Sin parametros (price)",403)
        # Cast price to float
        try:
            float(request.form['price'])
            # Price > 0
            if float(request.form['price']) <= 0:
                return responseJSON(None,"Precio invalido",403)
        except ValueError:
            return responseJSON(None,"Parametros invalidos (price)",403)
        # CATEGORY
        if not "category_id" in request.form:
            return responseJSON(None,"Sin parametros (category_id)",403)
        # Cast to int
        try:
            int(request.form['category_id'])
        except ValueError:
            return responseJSON(None,"Parametros invalidos (category_id)",403)

        # Add property
        new_property = Property(request.form['name'],request.form['description'],request.form['surface'],request.form['price'],request.form['category_id'],0)
        db.session.add(new_property)
        db.session.commit()
        return responseJSON(propertyToJSON(new_property),None,200) 

    # Edit property
    def put(self, id):
        if id:
            property = Property.query.get(id)
            if not property:
                return responseJSON(None,"Parametros invalidos (id)",403)
            # NAME
            if not request.form:
                return responseJSON(None,"Sin parametros (name)",403)
            if not "name" in request.form:
                return responseJSON(None,"Parametros invalidos (name)",403)
            # Check for name not null
            if len(request.form['name']) < 1:
                return responseJSON(None,"Nombre invalido",403)
            # DESCRIPTION
            if not "description" in request.form:
                return responseJSON(None,"Parametros invalidos (description)",403)
            if len(request.form['description']) < 1:
                return responseJSON(None,"Descripcción invalida",403)
            # SURFACE
            if not "surface" in request.form:
                return responseJSON(None,"Parametros invalidos (surface)",403)
            if int(request.form['surface']) < 60:
                return responseJSON(None,"Superficie invalida",403)   
            # PRICE
            if not "price" in request.form:
                return responseJSON(None,"Sin parametros (price)",403)
            # Cast price to float
            try:
                float(request.form['price'])
                # Price > 0
                if float(request.form['price']) <= 0:
                    return responseJSON(None,"Precio invalido",403)
            except ValueError:
                return responseJSON(None,"Parametros invalidos (price)",403)
            # CATEGORY
            if not "category_id" in request.form:
                return responseJSON(None,"Sin parametros (category_id)",403)
            # Cast to int
            try:
                int(request.form['category_id'])
            except ValueError:
                return responseJSON(None,"Parametros invalidos (category_id)",403)

            # Create property
            property.name        = request.form['name']
            property.description = request.form['description']
            property.surface       = request.form['surface']
            property.price       = request.form['price']
            property.category_id = request.form['category_id']
            db.session.add(property)
            db.session.commit()
            return responseJSON(propertyToJSON(property),None,200)
        return responseJSON(None,"Id invalido",403)



# Convert query of sqlalchemy to JSON
def propertyToJSON(property: Property):
    return {
                'id': property.id,
                'name': property.name,
                'description': property.description,
                'surface': property.surface,
                'price': property.price,
                'category_id': property.category.id,
                'category': property.category.name,
            }




# API credentials
api_username=os.getenv("API_USER")
api_password=os.getenv("API_PASSWORD")

# Protect API
def protectAPI(f):
    def propertyDecorated(*args,**kwargs):
        auth = request.authorization
        if api_username == auth.username and api_password == auth.password:
            return f(*args, **kwargs)
        # Unauthorized
        return abort(401)
    return propertyDecorated


### Routes ###
# property_view = PropertyAPI.as_view('property_view') # Unprotected API
property_view = protectAPI(PropertyAPI.as_view('property_view'))
# GET
app.add_url_rule('/api/properties/', view_func=property_view, methods=['GET','POST'])
# CRUD
app.add_url_rule('/api/properties/<int:id>', view_func=property_view, methods=['GET','POST','PUT','DELETE'])



