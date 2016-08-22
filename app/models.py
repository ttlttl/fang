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
    images = db.relationship('Image', backref='author', lazy='dynamic')

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
    en_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    areas = db.relationship('Area', backref='district', lazy='dynamic')

    @staticmethod
    def insert_districts():
        districts = [('黄埔区', 'huangpuqu'), ('徐汇区', 'xuhuiqu'), ('长宁区', 'changningqu'), \
                     ('静安区', 'jinganqu'), ('普陀区', 'xuhuiqu'), ('虹口区', 'hongkouqu'), \
                     ('闵行区', 'minhangqu'),('杨浦区', 'yangpuqu'), ('宝山区', 'baoshanqu'),\
                     ('嘉定区', 'jiadingqu'), ('浦东新区', 'pudongxinqu'), ('金山区', 'jinshanqu'),\
                     ('松江区','songjiangqu'), ('青浦区', 'qingpuqu'), ('奉贤区', 'fengxianqu'),\
                     ('崇明县', 'chongmingxian')]
        for name, en_name in districts:
            district = District.query.filter_by(name=name).first()
            if district is None:
                district = District(name=name, en_name=en_name)
                db.session.add(district)
        db.session.commit()

    def __repr__(self):
        return self.name


class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    en_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    communities = db.relationship('Community', backref='area', lazy='dynamic')

    @staticmethod
    def insert_areas():
        qingpu = ['白鹤', '华新镇', '青浦新城', '徐泾', '朱家角', '赵巷', '重固', '其他']
        hongkou = ['北外滩', '临平路', '四川北路', '其他']
        districts = {'青浦区': qingpu, '虹口区': hongkou}
        for district, areas in districts.items():
            d = District.query.filter_by(name=district).first()
            for area in areas:
                a = Area(name=area, district=d)
                db.session.add(a)
        db.session.commit()

    def __repr__(self):
        return self.name


class Community(db.Model):
    __tablename__ = 'communities'
    id = db.Column(db.Integer, primary_key=True)
    en_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    houses = db.relationship('House', backref='community', lazy='dynamic')

    def __repr__(self):
        return self.name


class HouseType():
    gongyu = 1
    bieshu = 2
    zhuzhai = 3
    laogongfang = 4
    yangfang = 5
    pingfang = 6
    other = 99


class HouseDecoration():
    maopi = 1
    jiandan = 2
    zhongdeng = 3
    jingzhuang = 4
    haohua = 5
    other = 99


class HouseToward():
    """
    House toward, E = East, W = West ...
    """
    E = 1
    W = 2
    S = 3
    N = 4
    ES = 5
    EN = 6
    WS = 7
    EN = 8



class House(db.Model):
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    is_new = db.Column(db.Boolean, default=True)
    completion_time = db.Column(db.DateTime)
    type = db.Column(db.SmallInteger)
    decoration = db.Column(db.SmallInteger)
    toward = db.Column(db.SmallInteger)
    floor = db.Column(db.SmallInteger)
    total_floor = db.Column(db.SmallInteger)
    shi = db.Column(db.SmallInteger)
    ting = db.Column(db.SmallInteger)
    wei = db.Column(db.SmallInteger)
    price = db.Column(db.Integer)
    total_area = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    down_payment = db.Column(db.Integer)
    detail = db.Column(db.Text)
    hot = db.Column(db.SmallInteger, default=1)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='house', lazy='dynamic')


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))