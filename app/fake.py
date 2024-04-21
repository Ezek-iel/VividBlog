import os,sys
import uuid
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Blog, User, Comment
from app import db

# TODO Update fake data to existing database schema and save in database

def generate_random_user_id():
    return random.choice([user.id for user in User.query.all()])

def generate_random_blog_id():
    return random.choice([blog.id for blog in Blog.query.all()])

def generate_fake_blogs():
    f = Faker()
    count = 0
    while count < 1000:
        content = f.paragraphs(nb = 3)
        blog_to_add = Blog(id = str(uuid.uuid4()),title = f.sentence(nb_words = 6, variable_nb_words = True), post = ("\n").join(content), created = f.date_time_this_year(before_now=True, after_now=False, tzinfo=None), author_id = generate_random_user_id())

        db.session.add(blog_to_add)
        count += 1
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            print(error._message())
            continue

def generate_fake_users():

    f = Faker()
    count = 0
    while count < 200:
        
        user_to_add = User(id = str(uuid.uuid4()),username = f.first_name(), emailaddress = f.ascii_email(), password = f.pystr(min_chars=18, max_chars=20, prefix='', suffix=''), date_joined = f.date_time_between(start_date='-5y', end_date='now', tzinfo=None))

        db.session.add(user_to_add)
        count += 1

        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            print(error._message())
            continue

def generate_fake_comments():

    f = Faker()
    count = 0
    while count < 2000:

        comment_to_add = Comment(id = str(uuid.uuid4()), message = f.sentence(nb_words = 12, variable_nb_words = True), date_written = f.date_time_this_year(before_now=True, after_now=False, tzinfo=None), blog_id = generate_random_blog_id(), author_id = generate_random_user_id())

        count += 1
        db.session.add(comment_to_add)
        try:
            db.session.commit()
        
        except IntegrityError as error:
            db.session.rollback()
            print(error._message())
            continue

def update_comment_number():
    
    for blog in Blog.query.all():
        blog.comments_number = len(blog.comments)
        db.session.commit()
