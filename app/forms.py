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
    course = SelectField("Course", choices=[get_courses()])
    submit = SubmitField("Register course")


class CalenderEventForm(FlaskForm):
    event_date = DateTimeField("Datetime", format='%Y-%m-%d %H:%M:%s', validators=[DataRequired()] )
    event_description = TextAreaField("Description", validators=[InputRequired()])
    course = SelectField("Course", choices=[get_courses()])
    submit = SubmitField("Create calendar event")

    

class ForumForm(FlaskForm):
    forum_name = StringField("Name", validators=[InputRequired()])
    course = SelectField("Course", choices=[get_courses()])
    submit = SubmitField("Create forum")


class DiscussionThreadForm(FlaskForm):
    forum = SelectField("Forum ", choices=[get_forums()])
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Create thread")

class CommentForm(FlaskForm):
    thread = SelectField("Thread", choices= [get_threads()])
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Add reply")


class CourseContentForm(FlaskForm):
    course = SelectField("Course", choices=[get_courses()])
    section_no = SelectField("Section", choices=[range(1, 101)])
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Create course content")

class AssignmentForm(FlaskForm):
    course = SelectField("Course", choices=[get_courses()])
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    due_date = DateTimeField("Due date", format='%Y-%m-%d %H:%M:%s', validators=[DataRequired()])
    submit = SubmitField("Create assignment")

class SubmissionForm(FlaskForm):
    assignment = SelectField("Assignment", choices=[get_courses()])
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Submit")