from flask_login import UserMixin
from . import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    file = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(600), nullable=True)
    public = db.Column(db.Boolean, default = True) # Feature 4 from spec implementation
    category = db.Column(db.String(50), nullable=True) # Feature 3 from spec implementation

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'           : self.id,
           'name'         : self.name,
           'caption'      : self.caption,
           'file'         : self.file,
           'desc'         : self.description,
           'public'       : self.public, # Feature 4 from spec implementation
           'category'     : self.category # Feature 3 from spec implementation
       }
 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default = False)




