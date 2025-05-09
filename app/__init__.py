from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

app = Flask(__name__)

app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views











