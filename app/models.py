import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


def generate_random_id():
    return str(uuid.uuid4())


class Blog(db.Model):
    id = db.Column(db.String(36), default=generate_random_id, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    introduction = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=False)
    conclusion = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated = db.Column(db.DateTime(), nullable=True)
    likes = db.Column(db.Integer(), default=0)
    comments_number = db.Column(db.Integer(), default=0)

    author_id = db.Column(db.ForeignKey("user.id"), nullable=False)

    comments = db.relationship("Comment", backref="comment_author")

    @property
    def ingredients_involved(self):
        return self.ingredients.split(",")

    @ingredients_involved.setter
    def ingredients_involved(self, values):
        self.ingredients = ",".join(values)

    @property
    def steps_involved(self):
        return self.steps.split(",")

    @steps_involved.setter
    def steps_involved(self, values):
        self.steps = ",".join(values)


class User(db.Model):
    id = db.Column(db.String(36), default=generate_random_id, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email_address = db.Column(db.String(70), nullable=False)
    title = db.Column(db.String(90), nullable=False, default="Beginner")
    password_hash = db.Column(db.String(60), nullable=False)
    avatar_url = db.Column(db.String())
    date_joined = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    followers = db.Column(db.String(), default="", nullable=False)
    is_online = db.Column(db.Boolean(), default=False, nullable=False)
    last_online = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    blogs = db.relationship("Blog", backref="blog_author")

    @property
    def followers_list(self):
        return self.followers.split(",")

    @followers_list.setter
    def followers_list(self, values):
        self.followers = ", ".join(values)

    def add_follower(self, user_id):
        if user_id in self.followers_list:
            return

        if self.followers:
            self.followers += f",{user_id}"
        else:
            self.followers += f"{user_id}"

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, attempt):
        return check_password_hash(self.password_hash, attempt)

    @property
    def avatar_url(self):
        return "https://www.robohash.org/{0}".format(self.email_address)

    @avatar_url.setter
    def avatar_url(self, value):
        raise AttributeError("Change email to change avatar url")

    def ping(self):
        self.is_online = True
        self.last_online = datetime.now()

    def unping(self):
        self.is_online = False
        self.last_online = datetime.now()


class Comment(db.Model):
    id = db.Column(db.String(36), default=generate_random_id, primary_key=True)
    message = db.Column(db.Text)
    date_written = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    blog_id = db.Column(db.ForeignKey("blog.id"), nullable=False)
    author_id = db.Column(db.ForeignKey("user.id"), nullable=False)


class TokenBlackList(db.Model):
    id = db.Column(db.String(36), default=generate_random_id, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from app import db

def generate_random_id():
    return str(uuid.uuid4())

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.String(60), default = generate_random_id, primary_key = True)
    title = db.Column(db.String(),nullable = False)
    introduction = db.Column(db.Text, nullable = False)
    ingredients = db.Column(db.ARRAY(db.Text), nullable = True)
    steps = db.Column(db.ARRAY(db.Text), nullable = False)
    conclusion = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime(), default = datetime.now, nullable = False)
    updated = db.Column(db.DateTime(), nullable = True)
    likes = db.Column(db.Integer(), default = 0)
    comments_number = db.Column(db.Integer(), default = 0)

    author_id = db.Column(db.ForeignKey('users.id'), nullable = False)

    comments = db.relationship('Comment',backref = 'comment_author')
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(60), default = generate_random_id ,primary_key = True)
    username = db.Column(db.String(200), nullable =  False)
    email_address = db.Column(db.String(300), nullable = False)
    title = db.Column(db.String(200), nullable = False, default = 'Beginner')
    password_hash = db.Column(db.String(300), nullable = False)
    followers = db.Column(db.Integer(), default = 0)
    avatar_url = db.Column(db.String())
    date_joined = db.Column(db.DateTime(), default = datetime.now, nullable  = False)

    blogs = db.relationship('Blog', backref = 'blog_author')

    @property
    def password(self):
        raise AttributeError('Password cannot be accessed')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, attempt):
        return check_password_hash(self.password_hash, attempt)
    
    @property
    def avatar_url(self):
        return 'https://www.robohash.org/{0}'.format(self.email_address)
    
    @avatar_url.setter
    def avatar_url(self, value):
        raise AttributeError('Change email to change avatar url')
      
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(60), default = uuid.uuid4,primary_key = True)
    message = db.Column(db.Text)
    date_written = db.Column(db.DateTime(), default = datetime.now, nullable = False)
    blog_id = db.Column(db.ForeignKey('blogs.id'), nullable = False)
    author_id = db.Column(db.ForeignKey('users.id'), nullable = False)




    


    

