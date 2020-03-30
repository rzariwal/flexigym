# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
# postgres_local_base = 'postgresql://postgres:@localhost/'
# database_name = 'flask_jwt_auth'
postgres_local_base = 'postgresql://hello_flask:hello_flask@db:5432/'
database_name = 'hello_flask_prod'
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

print(SECRET_KEY)

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
