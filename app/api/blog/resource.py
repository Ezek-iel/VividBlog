from flask_restful import Resource
from flask import request, abort
from ...models import Blog, db, Comment
from ...schema import BlogItemSchema, CommentItemSchema, CreateCommentSchema, CreateBlogSchema
from marshmallow import ValidationError
import os
from dotenv import load_dotenv
from functools import cache
from datetime import datetime

load_dotenv()
SERVER_URL = os.getenv('SERVER_URL')


@cache
def get_blogs_number(query : str | None):
    """ summary_line
    * cached function to get the number of blogs satisfying a query. if no query, returns all
    
    Keyword arguments:
    
    query -- search query
    
    Return: Number of blogs satisfying the query or all if no query exists
    """
    
    if query:
        all_blogs = Blog.query.filter(Blog.title.like(f'%{query}%')).all()
        return len(all_blogs)
    else:
        all_blogs= Blog.query.all()
        return len(all_blogs)

class BlogItemResource(Resource):

    def get(self, blogid : str):
        blogneeded = Blog.query.filter_by(id = blogid).first()

        if blogneeded:
            blog_schema = BlogItemSchema()
            blog_dict = blog_schema.dump(blogneeded)
            blog_dict['comments_url'] = '{0}/blogs/{1}/comments'.format(SERVER_URL, blog_dict['id'])
            return blog_dict
        else:
            abort(404, 'Not Found')
    
    def put(self, blogid : str):
        blogneeded : Blog | None = Blog.query.filter_by(id = blogid).first()

        if blogneeded:
            data = request.get_json()
            blog_schema = CreateBlogSchema()

            try:
                new_blog = blog_schema.load(data)
            except ValidationError as error:
                abort(400, error.messages)
            
            blogneeded.title = new_blog.title
            blogneeded.post = new_blog.post
            blogneeded.updated = datetime.now()

            db.session.commit()
            return {'Message' : 'Operation Successful'}, 200
        else:
            abort(404, {'Message' : 'Not found'})

class BlogListResource(Resource):

    def get(self):
        
        """
        * Is paginated
        * URL parameters
        - query : search by blog title -> represented 'title'
        - page_set : current_page --> represented 'page'
        - page_number : Number of items in a page --> 'page_number'
        """
        
        query = request.args.get('title')
        page_set = request.args.get('page', 1)
        page_number = int(request.args.get('page_number', 10))

        if page_set:
            offset = page_number * (int(page_set) -  1)
        else:
            offset = 0
        
        count = get_blogs_number(query)
        total_pages = count // page_number

        # * next_page and previous_page url to enforce HATEOAS principles 
        if (int(page_set) + 1) > total_pages:
            next_page_url = None
        else:
            next_page_url = '{0}/blogs?page={1}'.format(SERVER_URL,(int(page_set) + 1))

        if int(page_set) == 1:
            previous_page_url = None
        else:
            previous_page_url = '{0}/blogs?page={1}'.format(SERVER_URL,int(page_set) - 1)

        # * Filter blogs according to query
        if query:
            all_blogs = Blog.query.filter(Blog.title.like(f'%{query}%')).offset(offset).limit(page_number).all()
            
        else:
            all_blogs = Blog.query.offset(offset).limit(page_number).all()
            
        
    
        blogschema = BlogItemSchema()
        all_blogs_list = []

        for blog in all_blogs:
            blog_dict = blogschema.dump(blog)
        
            # * insert urls to enable easy navigation for clients

            blog_dict['blog_url'] = '{0}/blogs/{1}'.format(SERVER_URL, blog_dict['id'])
            blog_dict['author_url'] = '{0}/users/{1}'.format(SERVER_URL, blog_dict['author_id'])
            all_blogs_list.append(blog_dict)
        
        return {
            'blogs' : all_blogs_list,
            'total_pages' : total_pages,
            'page' : page_set,
            'page_number' : page_number,
            'next_page' : next_page_url,
            'previous_page' : previous_page_url
        }
    
    def post(self):

        data = request.get_json()
        blog_schema = CreateBlogSchema()

        try:
            new_blog = blog_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)

        db.session.add(new_blog)
        db.session.commit()

        return {'Message' : 'Operation Successful'}, 200


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
        else:
            abort(404, "Not Found")
    
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


