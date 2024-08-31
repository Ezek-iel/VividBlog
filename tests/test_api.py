import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app import fake
from flask import current_app

class TestConfig(unittest.TestCase):
    
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()
        fake.generate_fake_users(20)
        fake.generate_fake_blogs(10)
        fake.generate_fake_comments(5)
    
    def test_app_is_not_none(self):
        self.assertIsNotNone(self.app)
    
    def test_app_config(self):
        self.assertTrue(current_app.config['TESTING'])
    
    def test_default_response(self):
        response = self.test_client.get('/api/v1/')
        self.assertEqual(response.status_code, 404)
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class BlogEndpointTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()
    
    def test_blog_endpoint(self):
        response = self.test_client.get('/api/v1/blogs')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_post(self):
        response = self.test_client.post('/api/v1/blogs')
        self.assertEqual(response.status_code, 401)
    
    def test_blog_post_with_data(self):
        response = self.test_client.post('/api/v1/blogs', json = {
            "title" : "A cat",
            "introduction" : "A cat likes to eat the following self.food",
            "author_id" : 1,
            "steps_involved" : ["Fry the eggs", "wash the stews", "Play new games"],
            "conclusion" : "Do nothing",
            "ingredients_involved" : ["chicken", "egg", "fish", "pepper"]
        })
        self.assertEqual(response.status_code, 401)
    
    def test_blog_post_with_invalid_data(self):
        response = self.test_client.post('/api/v1/blogs', json = {
            "title" : "A cat",
            "introduction" : "A cat likes to eat the following self.food",
            "author_id" : 1,
            "steps_involved" : ["Fry the eggs", "wash the stews", "Play new games"],
            "conclusion" : "Do nothing"
        })
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
class UserEndpointTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()
    
    def test_user_endpoint(self):
        response = self.test_client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
    
    def test_user_post(self):
        response = self.test_client.post('/api/v1/users', json = {})
        self.assertEqual(response.status_code, 400)
    
    def test_user_post_with_data(self):
        response = self.test_client.post('/api/v1/users', json = {
            "username" : "dog",
            "email_address" : "dog@dog.com",
            "password" : "eat",
            "title" : "Technical Writer"
        }
        )
        self.assertEqual(response.status_code, 201)
    def tearDown(self) -> None:
        db.drop_all()
        self.app_context.pop()
    
class CommentEndpointTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
    
    def test_comment_endpoint(self):
        response = self.test_client.get('/api/v1/comments')
        self.assertEqual(response.status_code, 404)
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
