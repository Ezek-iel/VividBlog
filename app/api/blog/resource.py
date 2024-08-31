import os
from datetime import datetime

from flask_restful import Resource
from flask import request, abort
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required

from ...schema import BlogItemSchema, CreateBlogSchema
from ...models import Blog, db, Comment


load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")


class BlogItemResource(Resource):

    def get(self, blogid: str):
        blog_needed = Blog.query.get_or_404(blogid)
        return {"blog" : BlogItemSchema().dump(blog_needed)}

    @jwt_required()
    def put(self, blogid: str):
        blog_needed = Blog.query.get_or_404(blogid)
        data = request.get_json()
        blog_schema = CreateBlogSchema()

        try:
            new_blog = blog_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        blog_needed.title = new_blog.title
        blog_needed.post = new_blog.post
        blog_needed.updated = datetime.now()

        db.session.commit()
        return {"Message": "Operation Successful"}, 200
        

    @jwt_required()
    def delete(self, blogid: str):
        blog_needed: Blog = Blog.query.get_or_404(blogid)
        db.session.delete(blog_needed)
        db.session.commit()
        return {"Message": "Operation successful"}, 200


class BlogListResource(Resource):

    def get(self):
        """
        ? 127.0.0.1:5000/blogs?title=cookie&currentPage=2&itemsPerPage=10
        * Is paginated
        * URL parameters
        - title : search by blog title -> represented 'title'
        - page_set : current_page --> represented 'currentPage'
        - page_number : Number of items in a page --> 'itemsPerPage'
        """

        title = request.args.get("title")
        current_page = request.args.get("currentPage", type=int, default=1)
        items_per_page = request.args.get("itemsPerPage", type=int, default=10)

        query = Blog.query
        next_url = None
        previous_url = None
        if title:
            query = query.filter(Blog.title.like(f"%{title}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

            if pagination.page > 1:
                previous_url = f"{SERVER_URL}/blogs/title={title}&currentPage={pagination.page - 1}&itemsPerPage={pagination.per_page}"

            if pagination.page < pagination.pages:
                next_url = f"{SERVER_URL}/blogs/title={title}&currentPage={pagination.page + 1}&itemsPerPage={pagination.per_page}"

        else:
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

            if pagination.page > 1:
                previous_url = f"{SERVER_URL}/blogs?currentPage={pagination.page - 1}&itemsPerPage={pagination.per_page}"

            if pagination.page < pagination.pages:
                next_url = f"{SERVER_URL}/blogs/?&currentPage={pagination.page + 1}&itemsPerPage={pagination.per_page}"
        
        return {
            "blogs" : [BlogItemSchema().dump(blog) for blog in pagination.items],
            "next_url" : next_url,
            "previous_url" : previous_url,
            "no of pages" : pagination.pages
        }

    @jwt_required()
    def post(self):

        data = request.get_json()
        blog_schema = CreateBlogSchema()

        try:
            new_blog = blog_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        db.session.add(new_blog)
        db.session.commit()

        return {"Message": "Operation Successful"}, 201
