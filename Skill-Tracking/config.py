# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cooperwashere'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://cooper:cooper12@localhost:5433/skill-tracking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
