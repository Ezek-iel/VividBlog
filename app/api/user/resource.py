import os
from functools import cache

from flask_restful import Resource
from flask import abort, request
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required

from ...models import User, db
from ...schema import UserItemSchema, CreateUserSchema, BlogItemSchema

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")


class UserItemResource(Resource):

    def get(self, userid):
        user_needed = User.query.get_or_404()
        return {"user" : UserItemSchema().dump(user_needed)}
    
    @jwt_required()
    def put(self, userid):
        data = request.get_json()
        user_needed = User.query.get_or_404(userid)


        user_schema = CreateUserSchema()
        try:
            new_user = user_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        user_needed.username = new_user.username
        user_needed.email_address = new_user.email_address
        user_needed.title = new_user.title

        db.session.commit()
        return {"Message": "Operation successful"}, 200
    
    @jwt_required()
    def delete(self, userid):
        user_needed = User.query.get_or_404(userid)

        db.session.delete(user_needed)
        db.session.commit()
        return {"Message": "Operation successful"}, 200


class UserListResource(Resource):

    def get(self):
        """
        * Is paginated
        * URL parameters
        - query : search by username -> represented 'username'
        - query : search by email_address -> represented 'emailAddress'
        - current_page : current_page --> represented 'currentPage'
        - items_per_page : Number of items in a page --> 'itemsPerPage'
        """

        username = request.args.get("username")
        email_address = request.args.get("emailAddress")
        current_page = request.args.get("currentPage", type=int, default=1)
        items_per_page = request.args.get("itemsPerPage", type=int, default=10)

        query = User.query
        next_url = None
        previous_url = None

        if username:
            query = query.filter(User.username.like(f"%{username}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

            if pagination.page > 1:
                previous_url = f"{SERVER_URL}/users/title={username}&currentPage={pagination.page - 1}&itemsPerPage={pagination.per_page}"

            if pagination.page < pagination.pages:
                next_url = f"{SERVER_URL}/users/title={username}&currentPage={pagination.page + 1}&itemsPerPage={pagination.per_page}"

        if email_address:
            query = query.filter(User.email_address.like(f"%{email_address}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

            if pagination.page > 1:
                previous_url = f"{SERVER_URL}/users/emailAddress={email_address}&currentPage={pagination.page - 1}&itemsPerPage={pagination.per_page}"

            if pagination.page < pagination.pages:
                next_url = f"{SERVER_URL}/blogs/emailAddress={email_address}&currentPage={pagination.page + 1}&itemsPerPage={pagination.per_page}"

        else:
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

            if pagination.page > 1:
                previous_url = f"{SERVER_URL}/users?currentPage={pagination.page - 1}&itemsPerPage={pagination.per_page}"

            if pagination.page < pagination.pages:
                next_url = f"{SERVER_URL}/users/?&currentPage={pagination.page + 1}&itemsPerPage={pagination.per_page}"

        return {
            "users": [UserItemSchema().dump(user) for user in pagination.items],
            "next_url": next_url,
            "previous_url": previous_url,
            "no of pages": pagination.pages,
        }

    def post(self):

        data = request.get_json()
        user_schema = CreateUserSchema()

        try:
            new_user = user_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        db.session.add(new_user)
        db.session.commit()
        return {"Message": "Operation Succesful"}, 201


class UserItemBlogs(Resource):

    def get(self, userid):

        user_needed = User.query.get_or_404(userid)
        user_blogs = user_needed.blogs

        print(user_blogs)

        return {'blogs' : [BlogItemSchema().dump(blog) for blog in user_blogs]}