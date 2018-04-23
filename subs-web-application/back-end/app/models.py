from datetime import datetime
from app import db

# All models inherit from the Base Flask-SqlAlchemy Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # This is a high-level view of the relationship between users and entries. For a one-to-many relationship, a db.relationship field is normally defined on the 'one' side and is used as a convenient way to get access to the 'many' side. 
    # Argument 1 = Which Model class represents the many side
    # Argument 2 = Defines the name of a field that will be added to the objects of the 'many' class that points back at the 'one' object. 
    # Argument 3 = Defines how the database query for the relationship will be issues
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    # This method tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(200))
    # Field will get indexed, useful for ordering and its utc time as default
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # This References an id value from the users table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Entry {}>'.format(self.details)