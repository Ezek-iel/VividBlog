from flask import Blueprint
from flask_restful import Api

comment_blueprint = Blueprint('comments',__name__)
comment_api = Api(comment_blueprint)

from . import endpoints, resource
