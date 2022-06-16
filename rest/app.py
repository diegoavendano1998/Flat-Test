
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


import os
import json

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)
db = SQLAlchemy(app)



# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
