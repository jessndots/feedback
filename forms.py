from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Optional, Email


class RegisterForm(FlaskForm):
    """Form for registering"""
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = EmailField("Email Address", validators=[InputRequired(), Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding feedback"""
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Feedback", validators=[InputRequired()])
