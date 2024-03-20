import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import schema
from app.models import Blog, Comment, User
import unittest

class TestBlogItemSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.b1 = Blog(id = 'welcome', title = 'Welcome to my blog',post = 'Welcome to my blog full content')
        self.bschema = schema.BlogItemSchema()
        self.bdump = self.bschema.dump(self.b1)

    def test_blog_dump_data_is_not_none(self):
        self.assertIsNotNone(self.bdump)
    
    def test_blog_dump_data_is_dictionary(self):
        self.assertIsInstance(self.bdump, dict)
    
    def test_blog_dump_data_is_correct(self):
        correct = {
            'id' : 'welcome',
            'title' : 'Welcome to my blog',
            'post' : 'Welcome to my blog full content',
            'created' : None,
            'updated' : None,
            'likes' : None,
            'comments_number' : None,
            'author_id': None
        }
        self.assertEqual(self.bdump, correct)

class TestCreateBlogItemSchema(unittest.TestCase):
    
    def setUp(self) -> None:
        self.sample_blog_data = {
            'title' : 'A very good blog',
            'post' : 'A very good blog content',
            'author_id' : '1'
        }
        self.schema = schema.CreateBlogSchema()
        self.blog = self.schema.load(self.sample_blog_data)
    
    def test_blog_load_data_is_not_none(self):
        self.assertIsNotNone(self.blog)
    
    def test_blog_load_data_is_blog_type(self):
        self.assertIsInstance(self.blog, Blog)

class TestCreateUserSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_user_data = {
            'username' : 'John jones',
            'emailaddress' : 'johnjones@gmail.com',
            'password' : 'dapassword',
            'title' : 'Mr'
        }
        self.schema = schema.CreateUserSchema()
        self.user = self.schema.load(self.sample_user_data)
    
    def test_user_load_data_is_not_none(self):
        self.assertIsNotNone(self.user)
    
    def test_user_load_data_is_blog_type(self):
        self.assertIsInstance(self.user, User)

class TestUserItemSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.u1 = User(username = 'John jones', emailaddress = 'john@jones.com',title = 'Mr.')
        self.uschema = schema.UserItemSchema()
        self.udump = self.uschema.dump(self.u1)

    def test_user_dump_data_is_not_none(self):
        self.assertIsNotNone(self.udump)
    
    def test_user_dump_data_is_dictionary(self):
        self.assertIsInstance(self.udump, dict)
    
    def test_user_dump_data_is_correct(self):
        correct = {
            'id' : None,
            'username' : 'John jones',
            'emailaddress' : 'john@jones.com',
            'title' : "Mr.",
            'followers' : None,
            'avatar_url' : 'https://www.gravatar.com/john@jones.com',
            'date_joined' : None
        }
        self.assertEqual(self.udump, correct)

class TestCreateCommentSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_comment_data = {
            'message' : 'A new comment',
            'author_id' : '4',
            'blog_id' : '7',
        }
        self.schema = schema.CreateCommentSchema()
        self.comment = self.schema.load(self.sample_comment_data)
    
    def test_comment_load_data_is_not_none(self):
        self.assertIsNotNone(self.comment)
    
    def test_comment_load_data_is_blog_type(self):
        self.assertIsInstance(self.comment, Comment)

class TestCommentItemSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.c1 = Comment(message = 'A new message', date_written = None,author_id = None, blog_id = None)
        self.cschema = schema.CommentItemSchema()
        self.cdump = self.cschema.dump(self.c1)

    def test_comment_dump_data_is_not_none(self):
        self.assertIsNotNone(self.cdump)
    
    def test_comment_dump_data_is_dictionary(self):
        self.assertIsInstance(self.cdump, dict)
    
    def test_comment_dump_data_is_correct(self):
        correct = {
            'id' : None,
            'message' : 'A new message',
            'date_written': None,
            'blog_id' : None,
            'author_id' : None 
        }
        self.assertEqual(self.cdump, correct)


if __name__ == '__main__':
    unittest.main()