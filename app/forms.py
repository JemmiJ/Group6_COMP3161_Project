from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField,DateTimeField
from wtforms.validators import InputRequired,DataRequired
from db import connectDB


"""Helper functions"""
def get_courses():
    try:
        db_connect= connectDB()
        cursor =  db_connect.cursor()
        course_query = "SELECT CCode, CName FROM CMS_Courses"
        cursor.execute(course_query)
        courses = cursor.fetchall()
        course_lst = [f"{course[0]} {course[1]}"for course in courses]
        return course_lst
    except Exception as err:
        print({"Error": err})

def get_forums():
    try:
        db_connect = connectDB()
        cursor = db_connect.cursor()
        forum_query = "SELECT ForumName FROM CMS_Forums"
        cursor.execute(forum_query)
        forums = cursor.fetchall()
        forum_lst = [forum for forum in forums]
        return forum_lst
    except Exception as err:
        return({"Error": err})
    
def get_threads():
    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()
        thread_query = "SELECT Title FROM CMS_Threads"
        cursor.execute(thread_query)
        threads = cursor.fetchall()
        thread_lst = [thread for thread in threads]
        return thread_lst
    except Exception as err:
        return ({"Error": err})

class LoginForm(FlaskForm):
    user_id = StringField('User_ID', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    user_id = StringField('User_ID', validators=[InputRequired()])
    first_name = StringField('First_Name', validators=[InputRequired()])
    last_name = StringField('Last_Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('lectuter', 'Lecturer'),('admin', 'Admin')])
    submit = SubmitField('Register')







