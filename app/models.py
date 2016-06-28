# -*- coding=UTF-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db, login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    actived = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    houses = db.relationship('House', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.is_admin

    # for unit test
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     name=forgery_py.name.full_name(),
                     password=forgery_py.lorem_ipsum.word(),
                     member_since=forgery_py.date.date(True),
                     )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.sessin.rollback()

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    db.relationship('Area', backref='district', lazy='dynamic')

    def __repr__(self):
        return self.name

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    db.relationship('Community', backref='area', lazy='dynamic')

    def __repr__(self):
        return self.name


class Community(db.Model):
    __tablename__ = 'communities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    position_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    db.relationship('House', backref='community', lazy='dynamic')

    def __repr__(self):
        return self.name


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    is_new = db.Column(db.Boolean, default=True)
    completion_time = db.Column(db.DateTime)
    kinds = db.Column(db.String(64), index=True)
    decorate = db.Column(db.String(64), index=True)
    direction = db.Column(db.String(64))
    floor = db.Column(db.Integer)
    total_floor = db.Column(db.Integer)
    shi = db.Column(db.Integer)
    ting = db.Column(db.Integer)
    wei = db.Column(db.Integer)
    price = db.Column(db.Integer)
    total_area = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    down_payment = db.Column(db.Integer)
    detail = db.Column(db.Text)
    hot = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


