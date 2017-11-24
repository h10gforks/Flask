#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

"""
development configuration
 -- DEBUG: debug mode
 -- SQLALCHEMY_DATABASE_URI:
    -- The database URI that should be used for the connection.
more connection URI format:
 -- Postgres:
    -- postgresql://scott:tiger@localhost/mydatabase
 -- MySQL:
    -- mysql://scott:tiger@localhost/mydatabase
 -- Oracle:
    -- oracle://scott:tiger@127.0.0.1:1521/sidname
"""
class DevelopmentConfig(Config):
    """development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")

"""
testing configuration
 -- TESTING: True
 -- WTF_CSRF_ENABLED:
    -- in testing environment, we don't need CSRF enabled
"""
class TestingConfig(Config):
    """testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-test.sqlite")
    WTF_CSRF_ENABLED = False

# production configuration

class ProductionConfig(Config):
    """production configuration"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "develop": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

