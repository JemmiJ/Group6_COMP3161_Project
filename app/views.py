import os
from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, jsonify,url_for,flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt 
from app.forms import LoginForm, RegisterForm, CourseForm,RegisterCourse
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
    """Retrieves a list of courses taught by a lecturer."""
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


@app_views.route("/api/course/<course_id>", methods=["POST"])
def get_course_members(course_id):
    """This function retrieves a list of students and lecturers enrolled in a course.
"""
    if request.method=="POST":
        try:
            db_connect = connectDB()
            cursor = db_connect.cursor()
            members_query = "SELECT FirstName ,LastName FROM CMS_Students  \
            INNER JOIN CMS_Enrolment on CMS_Students.StudID=CMS_Enrolment.StudID\
            INNER JOIN CMS_Courses on CMS_Enrolment.CID=CMS_Courses.CID \
            WHERE CMS_Courses.CID=%s\
            UNION SELECT LFirstName ,LLastname FROM CMS_Lecturers\
            INNER JOIN CMS_Teaches on CMS_Lecturers.LecID=CMS_Teaches.LecID \
            INNER JOIN CMS_Courses on CMS_Teaches.CID= CMS_Courses.CID \
            WHERE CMS_Courses.CID=%s"
            cursor.execute(members_query, (course_id, course_id))

            names_lst = []
            for first_name, last_name in cursor:
                name = {}
                name['Full_name'] = (first_name, last_name)
                names_lst.append(name)
            cursor.close()
            db_connect.close()
            return json.dumps(names_lst, sort_keys=False)
            
        except Exception as err:
            print({"Error": err})

@app_views.route("/api/register/course/<student_id>", methods=["POST"])
def register_course(student_id):
    """
    Registers a student for a course.
    """
    if request.method == "POST":
        form = RegisterCourse()
        if form.validate_on_submit():
            try:
                db_connect = connectDB()
                cursor = db_connect.cursor()
                course = form.course.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                insert_course = "INSERT INTO CMS_Enrolment(StudID, CID) VALUES(%s, %s)"
                cursor.execute(insert_course,(student_id, course_id) )
                cursor.close()
                db_connect.close()
            except Exception as err:
                  print({"Error": err})
    pass


@app_views.route("/calender_event/<course_id>", methods="POST")
def get_calender_events(course_id):
    if request.method =="POST":
        try:
            db_connect = connectDB()
            cursor = db_connect.cursor()

            calender_query = "SELECT * FROM CMS_Events WHERE CourseID =%s"
            cursor.execute(calender_query, (course_id))
            event_lst= []
            for event_ID, course_ID, event_Date, event_Description in cursor:
                event = {}
                event["eventID"] = event_ID
                event["CourseID"] = course_ID
                event["eventDate"] = event_Date
                event['eventDescription'] = event_Description
                event_lst.append(event)
            cursor.close()
            db_connect.close()
            return json.dumps(event_lst, sort_keys=False)
        except Exception as err:
            print({"Error":err})

@app_views.route("/calender_event/<calender_date>/<student_id>", methods="GET")
def get_student_events(calender_date,student_id):
    if request.method =="GET":
        try:
            db_connect = connectDB()
            students_events = "SELECT * from CMS_Events INNER JOIN CMS_Enrolment CMS_Events.CourseID=CMS_Enrolment.CID \
                WHERE CMS_Enrolment.StudID = %s AND CMS_Events.eventDate = %s"
            cursor = db_connect.cursor()
            cursor.execute(students_events, (student_id, calender_date))
            events = cursor.fetchall()
            return jsonify(events)
        
        except Exception as err:
            return jsonify({"Error":str(e)})