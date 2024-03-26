from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, abort
from flask_jwt_extended import jwt_required


from ...schema import CommentItemSchema, CreateCommentSchema
from ...models import Blog,Comment,db

class CommentsListResource(Resource):

    def get(self, blogid : str):        
        blog_needed = Blog.query.filter_by(id = blogid).first()

        if blog_needed:
            comments = blog_needed.comments
            commentschema = CommentItemSchema()
            comment_list = [commentschema.dump(comment) for comment in comments]

            return {
                'No of comments' : len(comment_list),
                'comments' : comment_list
            }
        else:
            abort(404, "Not Found")
    
    @jwt_required()
    def post(self, blogid : str):

        blog_needed = Blog.query.filter_by(id = blogid).first()
        data = request.get_json()
        
        if blog_needed:
            commentSchema = CreateCommentSchema()  
            try:
                new_comment = commentSchema.load(data)            
            except ValidationError as error:
                abort(400, error.messages)

            db.session.add(new_comment)
            db.session.commit()   
            return {'Message' : 'Operation Succesful'}, 200
       
        else:
            abort(404, 'Not found')


class CommentItemResource(Resource):

    def get(self, blogid : str, commentid : str):
        comment_needed = Comment.query.filter_by(id = commentid).first()

        if comment_needed:
            comment_schema = CommentItemSchema()
            comment_dict = comment_schema.dump(comment_needed)
            return comment_dict
        else:
            abort(404, 'Not Found')
    
    @jwt_required()
    def delete(self, blogid : str, commentid : str):
        comment_needed = Comment.query.filter_by(id = commentid).first()

        if comment_needed:
            db.session.delete(comment_needed)
            db.session.commit()
            return {'Message' : 'Operation successful'}, 200
        else:
            abort(404, {'Message' : 'Not found'})

