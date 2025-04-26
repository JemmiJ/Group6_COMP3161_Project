from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    user_id = StringField('User_ID', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    user_id = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First_Name', validators=[InputRequired()])
    last_name = StringField('Last_Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('lectuter', 'Lecturer'),('admin', 'Admin')])
    submit = SubmitField('Register')