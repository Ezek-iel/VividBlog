import os

from flask_restful import Resource
from flask import abort, request
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required

from ...models import User, db
from ...schema import UserItemSchema, CreateUserSchema, BlogItemSchema

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")

SERVER_URL = os.getenv("SERVER_URL")


class UserItemResource(Resource):

    def get(self, userid):
        user_needed = User.query.get_or_404()
        return {"user" : UserItemSchema().dump(user_needed)}
    
    @jwt_required()
    def put(self, userid):

        data = request.json()
        
        user_needed = User.query.get_or_404(userid)
        try:
            UserItemSchema.load(data, instance = user_needed, partial = True) 
        except ValidationError as error:
            abort(400, error.messages)      
        
        db.session.commit()

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

        # * Collect all query parameters
        query = User.query
        username = request.args.get("username")
        email = request.args.get("email")
        title = request.args.get("title")
        page = request.args.get("page")
        items_per_page = request.args.get("pageNumber")

        #* Update query for filtering results
        if username:
            query = query.filter(User.username.like(f"%{username}%"))

        if email:
            query = query.filter(User.email_address.like(f"%{email}%"))

        if title:
            query = query.filter(User.title.like(f"%{title}%"))

        #* Paginate the results
        pagination = query.paginate(page = page, per_page=items_per_page, error_out=True)

        all_users = [UserItemSchema().dump(user) for user in pagination.items]

        return {
            "users" : all_users,
            "page" : pagination.page,
            "total_pages" : pagination.pages
        }


    def post(self):

        data = request.get_json()
        user_schema = CreateUserSchema()

        try:
            new_user = user_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        if User.query.filter_by(username = new_user.username).first() or User.query.filter_by(email_address = new_user.email_address).first():
            abort(400, {'Message' : 'User already exists'})
    
        db.session.add(new_user)
        db.session.commit()
        return {"Message": "Operation Succesful"}, 200


class UserItemBlogs(Resource):

    def get(self, userid):

        user_needed = User.query.get_or_404(userid)

        blogs = user_needed.blogs
        all_blogs = [BlogItemSchema().dump(blog) for blog in blogs]

        return all_blogs