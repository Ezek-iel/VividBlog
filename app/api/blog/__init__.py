from flask import Blueprint
from flask_restful import Api

blog_blueprint = Blueprint("blog",__name__)
blog_api = Api(blog_blueprint)

from . import endpoints,resource

