import re

from flask_wtf import FlaskForm
from flask import g
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError
from helpers import current_names

# Custom validator to ensure the last and first names of users only contain letters
def name_validator(form, field):
    name = field.data
    if not re.search(r'[a-zA-Z]', name):
        raise ValidationError('Name must contain only letters')

# Custom validator to ensure that user names are unique for every user
def user_name_validator(form, field):
    user_name = field.data
    existing_username = g.db.execute("SELECT * FROM users WHERE user_name = ?", user_name)
    if existing_username:
        raise ValidationError('User name already exists, please use another one.')

# Custom validators for passwords
def password_validator(form, field):
    password = field.data
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search (r'[!@#$%^&amp;*(),.?":{}|&lt;&gt;]', password):
        raise ValidationError('Password must contain atleast one speacial character') 
           

#Create a Form Class
class CreateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), name_validator])
    last_name = StringField('Last Name', validators=[InputRequired(), name_validator])
    user_name = StringField('User Name', validators=[InputRequired(), user_name_validator])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('verify_password', message="Passwords do no match"), Length(min=8, message='Password must be atleast 8 characters long'), password_validator])
    verify_password = PasswordField('Repeat Password', validators=[InputRequired(message='Please repeat the new password')])


