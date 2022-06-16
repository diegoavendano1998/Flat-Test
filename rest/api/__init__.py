
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


import os

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)
db = SQLAlchemy(app)



from api.utils.populate_db import populate_users,populate_categories,populate_properties
# create the DB on demand
@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    populate_users()
    populate_categories()
    populate_properties()



from api.rest_controller.user_controller import UserController
api.add_resource(UserController, '/users/')