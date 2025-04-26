from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired
from db import connectDB


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


class CourseForm(FlaskForm):
    def get_lecturers():
        try:
            db_connect = connectDB()
            cursor= db_connect.cursor()
            lecturer_query = "SELECT LFirstName, LLastName FROM CMS_Lecturers"
            cursor.execute(lecturer_query)
            lecturers = cursor.fetchall()
            lecturer_lst = [("{0}", "{1}").format(lecturer[0], lecturer[1])for lecturer in lecturers]
            return lecturer_lst
        except Exception as err:
            print({"Error": err})
    course_code =  StringField("Course_code", validators=[InputRequired()])
    course_name = StringField("Course_name", validators=[InputRequired()])
    department = SelectField("Department", choices=[("Science and Technology"), ('Social Sciences'), ('Medical Sciences')])
    lecturer = SelectField("Lecturer", choices=[get_lecturers()])
    submit = SubmitField("Create course")
    pass

class RegisterCourse(FlaskForm):
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
    
    course = SelectField("Course", choices=[get_courses()])
    submit = SubmitField("Register course")



    



