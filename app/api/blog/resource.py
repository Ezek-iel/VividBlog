from flask_restful import Resource
from flask import request, abort
from ...models import Blog, db
from ...schema import BlogItemSchema, CommentItemSchema

class BlogItemResource(Resource):

    def get(self, blogid : str):
        blogneeded = Blog.query.filter_by(id = blogid).first()

        if blogneeded:
            bschema = BlogItemSchema()
            blog_dict = bschema.dump(blogneeded)
            return blog_dict
        else:
            abort(404, 'Not Found')

class BlogListResource(Resource):

    def get(self):
        blogschema = BlogItemSchema()
        all_blogs = Blog.query.all()
        all_blogs_list = []
        for blog in all_blogs:
            blog_dict = blogschema.dump(blog)
            blog_dict['blog_url'] = 'http://127.0.0.1:5000/api/v1/blogs/{0}'.format(blog_dict['id'])
            all_blogs_list.append(blog_dict)
        return {
            'blogs' : all_blogs_list
        }

class BlogCommentsResource(Resource):

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

