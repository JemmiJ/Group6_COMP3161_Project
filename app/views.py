import os
from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app.forms import LoginForm, Registration
import pymysql
import jwt, datetime
from app.utils import token_required

app_views = Blueprint('app_views', __name__)
def dbconnect():
    return pymysql.connect(
        user='CMS_ADMIN', 
        password= app.config['PASSWORD'], 
        host='localhost', 
        database='CourseManagementSystem',
        auth_plugin='mysql_native_password'
    )


@app_views.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()
    userdb = dbconnect()
    cursor = userdb.cursor()

    if form.validate_on_submit():
        username = form.username.data
        user_password = form.password.data
        
        query = "SELECT * FROM CMS_Account WHERE AccName = %s"
        cursor.execute(query, (username))
        