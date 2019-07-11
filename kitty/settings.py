import os
import logging
from environs import Env

env = Env()
env.read_env()


DOC_TITLE = env.str('DOC_TITLE')
DOC_VERSION = env.str('DOC_VERSION')
DOC_URL = env.str('DOC_URL')


FLASK_STRICT_SLASHES = env.str('FLASK_STRICT_SLASHES')


class DefaultConfig:
    DEBUG = env.bool('DEBUG', default=False)
    SECRET_KEY = env.str('FLASK_SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_POOL_SIZE = env.int('SQLALCHEMY_POOL_SIZE', 50)
    SQLALCHEMY_POOL_RECYCLE = env.int("SQLALCHEMY_POOL_RECYCLE")


class TestConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_TEST_URI')
    SECRET_KEY = env.str('FLASk_TEST_SECRET_KEY', 'tesT')
