import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Blog, User, Comment
import unittest

# ! Each testcase maps to a model in the models.py file

u1 = User(username = 'dog', emailaddress = 'dog@dog.com',password = 'eat')
b1 = Blog(title = 'A cat', post = 'A cat likes to eat', author_id = u1)
c1 = Comment(message = 'A comment', blog_id = b1, author_id = u1)

class BlogTest(unittest.TestCase):

    def test_blog_is_not_none(self):
        self.assertIsNotNone(b1)
    
    def test_blog_has_author(self):
        self.assertIsNotNone(b1.author_id)
    
    def test_blog_author_is_user(self):
        self.assertIsInstance(b1.author_id, User)

class UserTest(unittest.TestCase):

    def test_user_is_not_none(self):
        self.assertIsNotNone(u1)
    
    def test_user_no_password_getter(self):
        with self.assertRaises(AttributeError):
            u1.password
    
    def test_users_password_hash_are_unequal(self):
        u2= User(username = 'cat', emailaddress = 'dog@cat.com',password = 'eat')
        self.assertNotEqual(u1.password_hash, u2.password_hash)
    
    def test_user_avatar_url(self):
        self.assertEqual(u1.avatar_url, 'https://www.gravatar.com/dog@dog.com')
    
    def test_user_verify_password(self):
        self.assertTrue(u1.verify_password('eat'))
    
    def test_no_avatar_url_setter(self):
        with self.assertRaises(AttributeError):
            u1.avatar_url = 'A random string'

class CommentTest(unittest.TestCase):

    def test_comment_is_not_none(self):
        self.assertIsNotNone(c1)    
   
if __name__ == '__main__':
    unittest.main()