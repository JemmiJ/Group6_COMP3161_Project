import os
from app import app, login_manager
from flask import render_template, request, redirect, jsonify,url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt 
from app.forms import LoginForm, RegisterForm
import pymysql
import jwt, datetime
from app.utils import token_required


bcrypt = Bcrypt(app) 

def connectDB():
    return pymysql.connect(
        user='CMS_ADMIN', 
        password= app.config['PASSWORD'], 
        host='localhost', 
        database='CourseManagementSystem',
        auth_plugin='mysql_native_password'
    )


@app.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()
    db = connectDB()
    cursor = db.cursor()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_password = form.password.data
        query = "SELECT * FROM CMS_Account WHERE AccName = %s"
        cursor.execute(query, (user_id))
        account = cursor.fetchone()
        if account:
            if bcrypt.check_password_hash(user_password, account.password):
                login_user(account)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'fail')
        else:
            flash('User not found', 'fail')
    return render_template('login/login.html', form=form)




@app.route('/register', methods=['POST'])
def user_register():
    try:
        form = RegisterForm()
        db= connectDB()
        cursor = db.cursor()
        if form.validate_on_submit():
            user_id = form.user_id.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8') 

            acc_insert = "INSERT INTO CMS_Account (AccID, AccPassword) VALUES (%s, %s)"
            cursor.execute(acc_insert, (user_id, hashed_password ))

            if request.form['role'] == 'Student':
                student_insert= "INSERT INTO CMS_Students(StudID, FirstName, LastName) VALUES (%s, %s, %s)"
                cursor.execute = (student_insert, (user_id, first_name, last_name))
            
            elif request.form['role']== 'Lecturer':
                lecturer_insert = "INSERT INTO CMS_Lecturers(LecID,LFirstName,LLastname ,Department) VALUES (%s,%s,%s,%s)"
                cursor.execute = (lecturer_insert, (user_id, first_name, last_name, request.form['Department']))

            db.commit()
            return redirect(url_for('user_login'))
        return render_template('signup/signup.html', form=form)
    except Exception as err:
        print({"Error": err})



