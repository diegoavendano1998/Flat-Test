from flask_restful import Resource,reqparse
from flask import request
from api.models.user import User


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('email', type=str)

class UserController(Resource):
    def get(self):
        response = []
        users = User.query.all()
        for user in users:
            response.append(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            )
        return response, 200
