import os
from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, jsonify,url_for,flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt 
from app.forms import LoginForm, RegisterForm, CourseForm
import jwt, datetime,json
from app.utils import token_required
from db import connectDB

app_views = Blueprint('app_views', __name__)
bcrypt = Bcrypt(app) 


@app_views.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()
    db_connect = connectDB()
    cursor = db_connect.cursor()
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
    return render_template('login.html', form=form)




@app_views.route('/register', methods=['POST'])
def user_register():
    try:
        form = RegisterForm()
        db_connect= connectDB()
        cursor = db_connect.cursor()
        if form.validate_on_submit():
            user_id = form.user_id.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

            acc_insert = "INSERT INTO CMS_Account (AccID, AccPassword) VALUES (%s, %s)"
            cursor.execute(acc_insert, (user_id, hashed_password ))

            if request.form['role'] == 'Student':
                student_insert= "INSERT INTO CMS_Students(StudID, FirstName, LastName) VALUES (%s, %s, %s)"
                cursor.execute = (student_insert, (user_id, first_name, last_name))
            
            elif request.form['role']== 'Lecturer':
                lecturer_insert = "INSERT INTO CMS_Lecturers(LecID,LFirstName,LLastname ,Department) VALUES (%s,%s,%s,%s)"
                cursor.execute = (lecturer_insert, (user_id, first_name, last_name, request.form['Department']))

            db_connect.commit()
            return redirect(url_for('user_login'))
        return render_template('signup.html', form=form)
    except Exception as err:
        print({"Error": err})

#how to get the id for the account
@login_required
@app_views.route('/create/course', methods=['POST'])
def create_course():
    if request.form['role'] == 'Admin':
        try:
            form = CourseForm()
            db_connect = connectDB()
            cursor = db_connect.cursor()

            if form.validate_on_submit():
                course_code = form.course_code.data
                course_name = form.course_name.data
                department = form.department.data
                lecturer_name = form.lecturer.data
                def get_lecturer_id(name):
                    db_connect = connectDB()
                    cursor = db_connect.cursor()
                    lec_query = "SELECT LecID FROM CMS_Lecturers WHERE LFirstName= AND    LLastname= "
                    return id
                
                lecturer_id = get_lecturer_id(lecturer_name)

                course_insert = "INSERT INTO CMS_Courses(CName,CCode,CDepartment, LecID) VALUES (%s, %s, %s, %s)"
                cursor.execute(course_insert, (course_name, course_code, department, lecturer_id))

                db_connect.commit()
                return redirect(url_for('create_course'))

                pass
        except:
            pass



@login_required
@app_views.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for("user_login"))
    

#Retrieve Courses
@app_views.route("/api/courses", methods=["GET"])
def get_courses():
    if request.method== 'GET':
        try:
            db_connect = connectDB()
            cursor = db_connect.cursor()

            courses_query = "SELECT * FROM CMS_Courses"
            cursor.execute(courses_query)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course[' CName '] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_connect.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})


@app_views.route("/api/courses/<student_id>", methods=['POST'])
def get_student_courses(student_id):
    if request.method =='POST':
        try:
            db_connect = connectDB()
            cursor = db_connect.cursor()

            student_courses = "SELECT CID,CName,CCode,CDepartment,LecID  FROM CMS_Courses INNER JOIN CMS_Enrolment on  CMS_Courses.CID=CMS_Enrolment.CID WHERE CMS_Enrolment.StudID={0}".format(student_id)
            cursor.execute(student_courses)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course[' CName '] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_connect.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})        

@app_views.route("/api/courses/<lecturer_id>", methods=['POST'])
def get_lecturer_courses(lecturer_id):
    if request.method =='POST':
        try:
            db_connect = connectDB()
            cursor = db_connect.cursor()

            courses_taught = "SELECT CID,CName,CCode,CDepartment,LecID FROM CMS_Courses WHERE LecID={0}".format(lecturer_id)
            cursor.execute(courses_taught)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course['CName'] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_connect.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})  

