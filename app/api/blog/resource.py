from flask_restful import Resource
from flask import request
from ...models import Blog, db

class BlogListResource(Resource):

    def get(self):
        all_blogs = Blog.query.all()
        blog_list = [blog.to_dict() for blog in all_blogs]
        return blog_list
    
    def post(self):
        form = request.form
        blogToAdd = Blog(title = form['title'], post = form['content'])
        db.session.add(blogToAdd)
        db.session.commit()

        blogInfo = Blog.query.filter_by(title = form['title']).first_or_404()
        return {
            "blog" : {
                "url" : f"/api/v1/blogs/{blogInfo.id}",
                "written by" : "Someone",
                "created at" : f"{blogInfo.created}"
            }
        }, 200
