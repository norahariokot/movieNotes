import re

from flask_wtf import FlaskForm
from flask import g
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError
from werkzeug.security import check_password_hash

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
    first_name = StringField('First Name', validators=[InputRequired(), name_validator], render_kw={"class": "create-acc-form-ctl"})
    last_name = StringField('Last Name', validators=[InputRequired(), name_validator], render_kw={"class": "create-acc-form-ctl"})
    user_name = StringField('User Name', validators=[InputRequired(), user_name_validator], render_kw={"class": "create-acc-form-ctl"})
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('verify_password', message="Passwords do no match"), Length(min=8, message='Password must be atleast 8 characters long'), password_validator], render_kw={"class": "create-acc-form-ctl"})
    verify_password = PasswordField('Verify Password', validators=[InputRequired(message='Please repeat the new password')], render_kw={"class": "create-acc-form-ctl"})


# Custom validator for username verification at login
def login_username_validator(form, field):
    login_username = field.data
    existing_user = g.db.execute("SELECT * FROM users WHERE user_name = ?", login_username)
    if not existing_user:
        raise ValidationError('Invalid user name')

# Custom validator for password at user login 
def login_password_validator(form, field):
    username = form.user_name.data
    password = field.data
   
    # Check user details in the database
    user = g.db.execute("SELECT * FROM users WHERE user_name = ?", username)  
    
    # Verify password  
    if not user or not check_password_hash(user[0]['hash'], password):
        raise ValidationError('Invalid password.') 

# Create a Form Class for the login form
class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired(), login_username_validator], render_kw={"class": "login-form-ctl"})
    password = PasswordField('Password', validators=[InputRequired(), login_password_validator], render_kw={"class": "login-form-ctl"})



