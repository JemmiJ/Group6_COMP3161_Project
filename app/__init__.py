from flask import Flask
from flask_login import LoginManager, UserMixin
from app.db import connectDB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager
from .config import Config

app = Flask(__name__)

login_manager = LoginManager()
jwt = JWTManager()

app.config.from_object(Config)

jwt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'app_views.login'

class User(UserMixin):
    def __init__(self, user_id, role):
        self.id = user_id  # Must be `id` for Flask-Login
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    
    # Verify user exists and fetch role
    cursor.execute("SELECT AccID FROM CMS_Account WHERE AccID = %s", (user_id,))
    if cursor.fetchone() is None:
        return None

    cursor.execute("SELECT StudID FROM CMS_Students WHERE StudID = %s", (user_id,))
    if cursor.fetchone():
        role = 'student'
    else:
        cursor.execute("SELECT LecID FROM CMS_Lecturers WHERE LecID = %s", (user_id,))
        if cursor.fetchone():
            role = 'lecturer'
        else:
            cursor.execute("SELECT AdminID FROM CMS_Admin WHERE AdminID = %s", (user_id,))
            if cursor.fetchone():
                role = 'admin'
            else:
                return None

    return User(user_id, role)

from app.views import app_views
app.register_blueprint(app_views)












