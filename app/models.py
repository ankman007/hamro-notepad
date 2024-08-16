from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')

# # TODO 
# class Reminder(db.Model, UserMixin):
#     pass 

# # TODO 
# # Allow users to attach files (e.g., images, PDFs) to their notes.
# class Attachment(db.Model, UserMixin):
#     pass 

# # TODO 
# class Category(db.Model, UserMixin):
#     pass 


