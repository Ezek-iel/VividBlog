import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Blog, User, Comment, generate_random_id
import unittest

# * Each testcase maps to a model in the models.py file

recipes = ['chicken', 'egg', 'fish', 'pepper']
steps = ['Fry the eggs', 'wash the stews', 'Play new games']
conclusion = "Do nothing"

u1 = User(username = 'dog', email_address = 'dog@dog.com',password = 'eat')
b1 = Blog(title = 'A cat', introduction = 'A cat likes to eat the following self.food', author_id = u1, steps_involved = steps, conclusion = conclusion, ingredients_involved = recipes)
c1 = Comment(message = 'A comment', blog_id = b1, author_id = u1)

class RandomIdTest(unittest.TestCase):

    def test_random_uuid(self):
        self.assertEqual(len(generate_random_id()), 36)


class BlogTest(unittest.TestCase):   

    def test_blog_is_not_none(self):
        self.assertIsNotNone(b1)
    
    def test_blog_has_author(self):
        self.assertIsNotNone(b1.author_id)
    
    def test_blog_author_is_user(self):
        self.assertIsInstance(b1.author_id, User)

    def test_ingredients_are_joined(self):
        result_value = 'chicken,egg,fish,pepper'
        self.assertEqual(b1.ingredients, result_value)

    def test_steps_are_joined(self):
        result_value = 'Fry the eggs,wash the stews,Play new games'
        self.assertEqual(b1.steps, result_value)
    
    def test_ingredients_involved_are_splitted(self):
        self.assertEqual(b1.ingredients_involved,b1.ingredients.split(","))
    
    def test_steps_involved_are_splitted(self):
        self.assertEqual(b1.steps_involved, b1.steps.split(","))

class UserTest(unittest.TestCase):

    def test_user_is_not_none(self):
        self.assertIsNotNone(u1)
    
    def test_user_no_password_getter(self):
        with self.assertRaises(AttributeError):
            u1.password
    
    def test_users_password_hash_are_unequal(self):
        u2= User(username = 'cat', email_address = 'dog@cat.com',password = 'eat')
        self.assertNotEqual(u1.password_hash, u2.password_hash)
    
    def test_user_avatar_url(self):
        self.assertEqual(u1.avatar_url, 'https://www.robohash.org/dog@dog.com')
    
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