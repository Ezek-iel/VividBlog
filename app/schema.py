import os, sys

from marshmallow import Schema, fields, post_load

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Blog, User, Comment

class CreateBlogSchema(Schema):
    """
    * Schema expected when recieving data from client
    """
    
    title = fields.String(required=True)
    introduction = fields.String(required=True)
    ingredients_involved = fields.List(fields.String(required=True))
    steps_involved = fields.List(fields.String(required=True))
    conclusion = fields.String(required=True)
    author_id = fields.String(required=True)

    @post_load
    def make_blog(self, data, **kwargs):
        return Blog(**data)

class BlogItemSchema(Schema):

    id = fields.String(required=True)
    title = fields.String(required=True)
    introduction = fields.String(required=True)
    ingredients_involved = fields.List(fields.String(required=True))
    steps_involved = fields.List(fields.String(required=True))
    conclusion = fields.String(required=True)
    created = fields.DateTime(required=True)
    updated = fields.DateTime()
    likes = fields.Integer()
    comments_number = fields.Integer()
    author_id = fields.String(required=True)

class CreateUserSchema(Schema):
    """
    * Schema expected when recieving data from client
    """
    username = fields.String(required=True)
    email_address = fields.Email(required = True)
    password = fields.String(required = True)
    title = fields.String(required = True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserItemSchema(Schema):
    
    id = fields.String(required=True)
    username = fields.String(required=True)
    email_address = fields.String(required=True)
    title = fields.String(required=True)
    followers = fields.Integer()
    avatar_url = fields.String(required=True)
    date_joined = fields.DateTime(required = True)

class CreateCommentSchema(Schema):
    """
    * Schema expected when recieving data from client
    """
    message = fields.String(required = True)
    author_id = fields.String(required = True)
    blog_id = fields.String(required = True)

    @post_load
    def make_comment(self, data, **kwargs):
        return Comment(**data)

class CommentItemSchema(Schema):
    
    id = fields.String(required=True)
    message = fields.String(required = True)
    author_id = fields.String(required = True)
    blog_id = fields.String(required = True)
    date_written = fields.String(required=True)
    

