from faker import Faker
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Blog
from app import db


def generate_fake_blogs():
    f = Faker()
    count = 0
    while count < 200:
        content = f.paragraphs(nb = 3)
        blog_to_add = Blog(title = f.sentence(nb_words = 6, variable_nb_words = True), post = ("\n").join(content), created = f.date_time_this_year(before_now=True, after_now=False, tzinfo=None))

        db.session.add(blog_to_add)
        count += 1
        try:
            db.session.commit()
        except:
            db.session.rollback()
            continue
