from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import TextArea

class RegisterUserForm(FlaskForm):
    '''Form for registering a new user'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])

class LoginForm(FlaskForm):
    '''Form for a user to login'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    '''Form for adding or editing Feedback'''

    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=100, message='Title must be 100 characters or less')])
    content = StringField('Content', validators=[InputRequired()], widget=TextArea())