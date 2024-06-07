import re
import logging
from datetime import datetime
from flask import flash

# Form validation utility functions
def is_valid_email(email):
    """
    Validate email address using regex.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def do_passwords_match(password, confirm_password):
    """
    Check if the password and confirm password match.
    """
    return password == confirm_password

# Database utility functions
def add_to_db(db, instance):
    """
    Add an instance to the database and commit the session.
    """
    db.session.add(instance)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding instance to DB: {e}")
        return False

def delete_from_db(db, instance):
    """
    Delete an instance from the database and commit the session.
    """
    db.session.delete(instance)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting instance from DB: {e}")
        return False

# Logging utility function
def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration.
    """
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

# Flash messages utility function
def flash_message(message, category='info'):
    """
    Flash a message to the user.
    """
    flash(message, category)

# Date and time utility functions
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """
    Format a datetime object as a string.
    """
    return value.strftime(format)

def parse_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """
    Parse a datetime string into a datetime object.
    """
    return datetime.strptime(value, format)
