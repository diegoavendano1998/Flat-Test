from flask.views import MethodView
from flask import request, abort
from sqlalchemy import exc

from api.models.category import Category
from api.helpers.request import responseJSON
from api import app, db

import os



class CategoryAPI(MethodView):
    # Find all categories
    def get(self,id=None):
        if id:
            category = Category.query.get_or_404(id)
            if not category:
                return responseJSON(None,"Parametros invalidos (id)",403)
            else:
                res = categoryToJSON(category)
        else:
            categories = Category.query.all()
            res=[]
            for p in categories:
                res.append(categoryToJSON(p))
        return responseJSON(res,None,200)

    
    # Add category
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
        
        # Add category
        new_category = Category(request.form['name'],request.form['description'],0)
        db.session.add(new_category)
        db.session.commit()
        return responseJSON(categoryToJSON(new_category),None,200) 


    # Edit category
    def put(self, id):
        if id:
            category = Category.query.get(id)
            if not category:
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

            # Create category
            category.name        = request.form['name']
            category.description = request.form['description']
            db.session.add(category)
            db.session.commit()
            return responseJSON(categoryToJSON(category),None,200)
            
        return responseJSON(None,"Id invalido",403)


    # Delete a category
    def delete(self, id):
        if id:
            try:
                category = Category.query.get_or_404(id)
                db.session.delete(category)
                db.session.commit()
                return responseJSON("Categoría eliminada",None,200)
            except exc.IntegrityError:
                return responseJSON(None,"No se puede eliminar una categoria con registros hijos",403)
        return responseJSON(None,"Parametros invalidos (id)",403)


# Convert query of sqlalchemy to JSON
def categoryToJSON(category: Category):
    return {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }



# API credentials
api_username=os.getenv("API_USER")
api_password=os.getenv("API_PASSWORD")

# Protect API
def protectAPI(f):
    def categoryDecorated(*args,**kwargs):
        auth = request.authorization
        if api_username == auth.username and api_password == auth.password:
            return f(*args, **kwargs)
        # Unauthorized
        return abort(401)
    return categoryDecorated


### Routes ###
# category_view = CategoryAPI.as_view('category_view') # Unprotected API
category_view = protectAPI(CategoryAPI.as_view('category_view'))
# GET
app.add_url_rule('/api/categories/', view_func=category_view, methods=['GET','POST'])
# CRUD
app.add_url_rule('/api/categories/<int:id>', view_func=category_view, methods=['GET','POST','PUT','DELETE'])

