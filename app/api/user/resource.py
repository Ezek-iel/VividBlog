from flask_restful import Resource
from ...models import User, db
from ...schema import UserItemSchema, CreateUserSchema
from flask import abort, request
from marshmallow import ValidationError

class UserItemResource(Resource):

    def get(self, userid):
        user_needed = User.query.filter_by(id = userid).first()
        if user_needed:
            uschema = UserItemSchema()
            user_dict = uschema.dump(user_needed)
            return user_dict
        else:
            abort(404, 'Not Found')

class UserListResource(Resource):

    def get(self):        
        userschema = UserItemSchema()
        all_users = User.query.all()
        all_users_list = []
        for user in all_users:
            user_dict = userschema.dump(user)
            user_dict['user_url'] = 'http://127.0.0.1:5000/api/v1/users/{0}'.format(user_dict['id'])
            all_users_list.append(user_dict)
        return {
            'users' : all_users_list
        }
    
    def post(self):
        data = request.get_json()
        u1 = CreateUserSchema()
        try:
            new_user = u1.load(data)
        except ValidationError as error:
            abort(400, error.messages)
        
        db.session.add(new_user)
        db.session.commit()
        return {'Message' : 'Operation Succesful'}, 200
