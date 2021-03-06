from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


users_tags = db.Table('users_tags',
                      db.Column('user_id', db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                      )

users_subreddits = db.Table('users_subreddits',
                            db.Column('user_id', db.Integer,
                                      db.ForeignKey('user.id')),
                            db.Column('subreddit_id', db.Integer,
                                      db.ForeignKey('subreddit.id'))
                            )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    send_email = db.Column(db.Boolean, default=False)
    last_email_sent = db.Column(db.DateTime, default=datetime.utcnow)

    tags = db.relationship(
        'Tag', secondary=users_tags, backref='taggers', lazy='dynamic'
    )
    subreddits = db.relationship(
        'Subreddit', secondary=users_subreddits, lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), index=True, unique=True)
    users = db.relationship('User', secondary=users_tags, lazy='dynamic')

    def __repr__(self):
        return f'<Tag {self.text}>'


class Subreddit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String(20), index=True, unique=True)
    users = db.relationship('User', secondary=users_subreddits, lazy='dynamic')

    def __repr__(self):
        return f'<Subreddit {self.sub}>'
