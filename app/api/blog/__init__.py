from flask import Blueprint

blog_blueprint = Blueprint("blog",__name__)

from . import endpoints,resource

