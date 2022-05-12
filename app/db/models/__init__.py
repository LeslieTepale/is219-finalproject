from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from app.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User %r>' % self.email

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    rating = db.Column(db.Integer, nullable=True, unique=False)
    review = db.Column(db.String, nullable=True, unique=False)
    date = db.Column(db.String, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="movies", uselist=False)

    def __init__(self, title, rating, review, date):
        self.title = title
        self.rating = rating
        self.review = review
        self.date = date

    def serialize(self):
        return {
            'title': self.title,
            'long': self.rating,
            'lat': self.review,
            'population': self.date,
        }

