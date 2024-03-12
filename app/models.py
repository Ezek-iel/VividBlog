from app import db
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    title = db.Column(db.String(),nullable = False)
    post = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime(), default = datetime.utcnow, nullable = False)
    updated = db.Column(db.DateTime(), nullable = True)

    def to_dict(self):
        return {"id" : self.id, "title" : self.title, "post" : self.post, "created" : str(self.created),"updated" : str(self.updated)}