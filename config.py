import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/production_app'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False