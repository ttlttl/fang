# -*- coding=UTF-8 -*-
"""
ADMIN_EMAIL: the administrator's email address.
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CACHE_TYPE = "simple"
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:hello@127.0.0.1/fang_dev"
    WHOOSH_BASE = "fang_dev"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:hello@127.0.0.1/fang_test"
    WHOOSH_BASE = "mysql+pymysql://test:hello@127.0.0.1/fang_test"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:hello@127.0.0.1/fang"
    WHOOSH_BASE = "mysql+pymysql://test:hello@127.0.0.1/fang"


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}