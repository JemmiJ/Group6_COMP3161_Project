import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads')))
    PASSWORD = os.environ.get('PASSWORD')