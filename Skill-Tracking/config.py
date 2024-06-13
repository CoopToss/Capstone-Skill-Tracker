import os

# Define the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cooperwashere'

    # PostgreSQL database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://cooper:cooper12@localhost:5432/skill-tracking'

    # Disable tracking modifications to avoid unnecessary overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False
