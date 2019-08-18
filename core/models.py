from datetime import datetime
from flask_login import UserMixin
from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_1.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    active = db.Column(db.Boolean, unique=False, default=True)
    admin_level = db.Column(db.Integer, unique=False, default=0)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.admin_level})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    source = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.fact}, {self.date_posted}"