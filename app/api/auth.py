from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from flask import request
from app import jwt, db

from ..models import User, TokenBlackList


@jwt.token_in_blocklist_loader
def check_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlackList.query.filter_by(jti=jti).first()
    return token is not None


class Login(Resource):

    def post(self):
        if not request.is_json:
            return {"Message": "Wrong media type"}, 415

        username = request.json["username"]
        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(request.json["password"]):
            access_token = create_access_token(identity=username)
            user.ping()
            db.session.commit()
            return {"access_token": access_token, "user_id": user.id}, 200
        elif not user:
            return {"Message": "User not found"}, 404
        elif not user.verify_password(request.json["password"]):
            return {"Message": "Incorrect password"}, 401


class Logout(Resource):

    @jwt_required()
    def post(self):
        data = request.json()
        print(data)
        jti = get_jwt()
        new_token = TokenBlackList(jti=jti["jti"])
        db.session.add(new_token)
        db.session.commit()
        return {"message": "Successfully logged out"}, 200


class CheckLogin(Resource):

    def post(self):
        data = request.get_json()
        id = data.get('id')
        user = User.query.get_or_404(id)
        return {"is_loggedin" : user.is_online}, 200   