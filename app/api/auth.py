from flask_httpauth import HTTPBasicAuth
from flask import g
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request

from ..models import User

class Login(Resource):

    def post(self):
        if request.is_json:
            username = request.json['username']
            user = User.query.filter_by(username = username).first()
        
        if user and user.verify_password(request.json['password']):
            access_token = create_access_token(identity = username)
            return {'access_token' : access_token}, 200
        elif not user:
            return {'Message' : 'User not found'}, 404
        elif not user.verify_password(request.json['password']):
            return {'Message' : 'Incorrect password'}, 401
       
    
