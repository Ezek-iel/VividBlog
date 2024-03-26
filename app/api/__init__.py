from flask import Blueprint
from flask_restful import Api

from .auth import Login

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from . import blog,user,comments
api_blueprint.register_blueprint(blog.blog_blueprint, url_prefix = "/blogs")
api_blueprint.register_blueprint(user.user_blueprint, url_prefix = "/users")
api_blueprint.register_blueprint(comments.comment_blueprint, url_prefix = '/comments')
api.add_resource(Login, "/auth/login")