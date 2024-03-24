import os
from functools import cache

from flask_restful import Resource
from flask import abort, request
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required

from ...models import User, db
from ...schema import UserItemSchema, CreateUserSchema, BlogItemSchema

load_dotenv()
SERVER_URL = os.getenv('SERVER_URL')

@cache
def get_users_number(query : str):
    """ summary_line
    * cached function to get the number of users satisfying a query. if no query, returns all
    
    Keyword arguments:
    
    query -- search query
    
    Return: Number of users satisfying the query or all if no query exists
    """
    if query:
        all_users = User.query.filter(User.username.like(f'%{query}%')).all()
        return len(all_users)
    else:
        all_users = User.query.all()
        return len(all_users)

class UserItemResource(Resource):

    def get(self, userid):
        user_needed = User.query.filter_by(id = userid).first()
        if user_needed:
            uschema = UserItemSchema()
            user_dict = uschema.dump(user_needed)
            return user_dict
        else:
            abort(404, 'Not Found')
    
    @jwt_required()
    def put(self, userid):
        data = request.get_json()
        userneeded = User.query.filter_by(id = userid).first()

        if userneeded:
            user_schema = CreateUserSchema()
            try:
                new_user = user_schema.load(data)
            except ValidationError as error:
                abort(400, error.messages)

            userneeded.username = new_user.username
            userneeded.emailaddress = new_user.emailaddress
            userneeded.title = new_user.title

            db.session.commit()
            return {'Message' : "Operation successful"}, 200
        else:
            abort(404, {'Message' : "Not found"})
    
    @jwt_required()
    def delete(self, userid):
        userneeded = User.query.filter_by(id = userid).first()

        if userneeded:
            db.session.delete(userneeded)
            db.session.commit()
            return {'Message' : 'Operation successful'}, 200
            
class UserListResource(Resource):

    def get(self):
        
        """
        * Is paginated
        * URL parameters
        - query : search by blog title -> represented 'title'
        - page_set : current_page --> represented 'page'
        - page_number : Number of items in a page --> 'page_number'
        """

        query = request.args.get('username')

        page_set = request.args.get('page', 1)
        page_number = int(request.args.get('page_size', 10))

        if page_set:
            offset = page_number * (int(page_set) - 1)
        else:
            offset = 0
        
        count = get_users_number(query)
        total_pages = count // page_number
        
        userschema = UserItemSchema()

        # * next page and previous page url to enforce HATEOAS principles
        if (int(page_set) + 1) > total_pages:
            next_page_url = None
        else:
            next_page_url = '{0}/users?page={1}&page_size={2}'.format(SERVER_URL, int(page_set) + 1, page_number)
        
        if int(page_set) == 1:
            previous_page_url = None
        else:
            previous_page_url = '{0}/users?page={1}&page_size={2}'.format(SERVER_URL, int(page_set) - 1, page_number)

        if query:
            all_users = User.query.filter(User.username.like(f'%{query}%')).offset(offset).limit(page_number).all()
        else:
            all_users = User.query.offset(offset).limit(page_number).all()

        all_users_list = []
        
        for user in all_users:
            user_dict = userschema.dump(user)

            # * insert urls to enable easy navigation for clients

            user_dict['user_url'] = '{0}/users/{1}'.format(SERVER_URL,user_dict['id'])
            all_users_list.append(user_dict)
        
        return {
            'users' : all_users_list,
            'total_pages' : total_pages,
            'page' : page_set,
            'page_number' : page_number,
            'next_page' : next_page_url,
            'previous_page': previous_page_url
        }
    
    def post(self):

        data = request.get_json()
        user_schema = CreateUserSchema()
        
        try:
            new_user = user_schema.load(data)
        except ValidationError as error:
            abort(400, error.messages)
        
        db.session.add(new_user)
        db.session.commit()
        return {'Message' : 'Operation Succesful'}, 200


class UserItemBlogs(Resource):

    def get(self, userid):

        userneeded = User.query.filter_by(id = userid).first()
        
        if not userneeded:
            abort(404, "Not found")
        else:
            blogschema = BlogItemSchema()
            userblogs = userneeded.blogs
            all_blogs_list = []
            
            for blog in userblogs:
                blog_dict = blogschema.dump(blog)

                # * insert urls to enable easy navigation for clients

                blog_dict['blog_url'] = '{0}/blogs/{1}'.format(SERVER_URL, blog_dict['id'])
                blog_dict['author_url'] = '{0}/users/{1}'.format(SERVER_URL, blog_dict['author_id'])
                all_blogs_list.append(blog_dict)
            return {
                'blogs' : all_blogs_list
            }