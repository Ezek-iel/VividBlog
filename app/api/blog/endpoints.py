from ...api import api
from .resource import BlogItemResource, BlogListResource

api.add_resource(BlogItemResource,'/blogs/<string:blogid>')
api.add_resource(BlogListResource,'/blogs')
