from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from . import blog,user
api_blueprint.register_blueprint(blog.blog_blueprint, url_prefix = "/blogs")
api_blueprint.register_blueprint(user.user_blueprint, url_prefix = "/users")