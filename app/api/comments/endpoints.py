from ...api import api
from .resource import CommentsListResource, CommentItemResource

api.add_resource(CommentsListResource, '/blogs/<string:blogid>/comments')
api.add_resource(CommentItemResource, '/blogs/<string:blogid>/comments/<string:commentid>')	
