import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

def generate_random_id():
    return str(uuid.uuid4())

class Blog(db.Model):
    id = db.Column(db.String(36), default = generate_random_id, primary_key = True)
    title = db.Column(db.String(),nullable = False)
    introduction = db.Column(db.Text, nullable = False)
    ingredients = db.Column(db.Text, nullable = True)
    steps = db.Column(db.Text, nullable = False)
    conclusion = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime(), default = datetime.now, nullable = False)
    updated = db.Column(db.DateTime(), nullable = True)
    likes = db.Column(db.Integer(), default = 0)
    comments_number = db.Column(db.Integer(), default = 0)

    author_id = db.Column(db.ForeignKey('user.id'), nullable = False)

    comments = db.relationship('Comment',backref = 'comment_author')

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
        self.steps =  ",".join(values)
    
class User(db.Model):
    id = db.Column(db.String(36), default = uuid.uuid4,primary_key = True)
    username = db.Column(db.String(40), nullable =  False)
    email_address = db.Column(db.String(70), nullable = False)
    title = db.Column(db.String(90), nullable = False, default = 'Beginner')
    password_hash = db.Column(db.String(60), nullable = False)
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
        return 'https://www.gravatar.com/{0}'.format(self.email_address)
    
    @avatar_url.setter
    def avatar_url(self, value):
        raise AttributeError('Change email to change avatar url')
      
class Comment(db.Model):
    id = db.Column(db.String(36), default = uuid.uuid4,primary_key = True)
    message = db.Column(db.Text)
    date_written = db.Column(db.DateTime(), default = datetime.now, nullable = False)
    blog_id = db.Column(db.ForeignKey('blog.id'), nullable = False)
    author_id = db.Column(db.ForeignKey('user.id'), nullable = False)




    


    

