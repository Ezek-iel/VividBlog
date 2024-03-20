from ...api import api
from .resource import BlogItemResource, BlogListResource, BlogCommentsResource

api.add_resource(BlogItemResource,'/blogs/<string:blogid>')
api.add_resource(BlogListResource,'/blogs')
api.add_resource(BlogCommentsResource, '/blogs/<string:blogid>/comments')
