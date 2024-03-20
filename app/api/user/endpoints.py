from ...api import api
from .resource import UserItemResource, UserListResource

api.add_resource(UserItemResource, '/users/<string:userid>')
api.add_resource(UserListResource, '/users')