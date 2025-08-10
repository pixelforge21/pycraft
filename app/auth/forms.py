from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class EnrollmentForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=120)])
    mobile = StringField("Mobile", validators=[DataRequired(), Length(min=6, max=20)])
    student_class = StringField("Class", validators=[DataRequired(), Length(min=1, max=30)])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=5, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Enroll")

