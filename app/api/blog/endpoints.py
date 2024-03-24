from ...api import api
from .resource import CommentItemResource, BlogItemResource, BlogListResource, CommentsListResource

api.add_resource(BlogItemResource,'/blogs/<string:blogid>')
api.add_resource(BlogListResource,'/blogs')
api.add_resource(CommentsListResource, '/blogs/<string:blogid>/comments')
api.add_resource(CommentItemResource, '/blogs/<string:blogid>/comments/<string:commentid>')	
