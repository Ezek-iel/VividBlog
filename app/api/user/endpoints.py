from ...api import api
from .resource import UserItemResource, UserListResource, UserItemBlogs

api.add_resource(UserItemResource, '/users/<string:userid>')
api.add_resource(UserListResource, '/users')
api.add_resource(UserItemBlogs, '/users/<string:userid>/blogs')