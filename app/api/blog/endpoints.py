from .resource import BlogListResource
from ...api import api

api.add_resource(BlogListResource,'/blogs')