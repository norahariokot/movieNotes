import re

from flask_wtf import FlaskForm
from flask import g
from flask import session
from wtforms import StringField, PasswordField, SubmitField, FileField, HiddenField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError
from flask_wtf.file import FileAllowed
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
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('verify_password', message="Passwords do no match"), Length(min=8, message='Password must be atleast 8 characters long'), password_validator], render_kw={"class": "create-acc-form-ctl create-user-password", "id": "password"})
    verify_password = PasswordField('Verify Password', validators=[InputRequired(message='Please repeat the new password')], render_kw={"class": "create-acc-form-ctl create-user-password"})


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
    password = PasswordField('Password', validators=[InputRequired(), login_password_validator], render_kw={"class": "login-form-ctl", "id":"login-password"})


# Custom validator for updating user profile info to ensure that an existing username belongs to current user
def update_username_validator(form, field):
    user_name = field.data
    current_user_id = int(form.current_user_id.data)
    print(f"Current user_id {type(current_user_id)}")

    # Query database to find user with the new username
    existing_username = g.db.execute("SELECT id FROM users WHERE user_name = ?", user_name)
    if existing_username:
        print(f"Existing user_id {type(existing_username[0]['id'])}")

    # Check if username exits and if it already belongs to the current user
    if existing_username and existing_username[0]['id'] != current_user_id:
        raise ValidationError('User name already exists, please use another one')


# Create a form class for update profile info form  
class UpdateUserProfile(FlaskForm):
    current_user_id = HiddenField()
    first_name = StringField('First Name', validators=[InputRequired(), name_validator], render_kw={"class": "profile-update-form-ctl"})
    last_name = StringField('Last Name', validators=[InputRequired(), name_validator], render_kw={"class": "profile-update-form-ctl"})
    user_name = StringField('User Name', validators=[InputRequired(), update_username_validator], render_kw={"class": "profile-update-form-ctl"})
 

# Create a form class for update profile picture
class UpdateProficPic(FlaskForm):
    current_user_id = HiddenField()
    profile_pic = FileField("Upload Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')], render_kw={"class": "profile-update-form-img", "id": "update-profilepic-input"})

# Custom validators for verify account form
# Custom validator for verifying user to ensure that their username actually exists in the database for user not yet logged in
def verify_username_validator(form, field):
    user_name = field.data
   
    # Query database to find user with the new username
    user_exists = g.db.execute("SELECT id FROM users WHERE user_name = ?", user_name)

    # Check if username exits 
    if not user_exists:
        raise ValidationError('User name is invalid!')

# Create a form class to verify user account before updating password
class VerifyUsername(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired(), verify_username_validator], render_kw={"class": "verify-username-form-ctl", "autocomplete": "off"})

# Custom validator for verifying user to ensure that their username actually exists and belongs to logged in user
def verify_loggedin_username_validator(form, field):
    user_name = field.data
    current_user_id = session.get('user_id') 

    # Query database to verify username for logged in user
    user_exists = g.db.execute("SELECT user_name FROM users WHERE id = ?", current_user_id)

    # Check if username exits and if it already belongs to the current user
    if user_exists and user_exists[0]['user_name'] != user_name:
        raise ValidationError('User name is invalid!')       

# Create a form class to verify user account before updating password
class VerifyLoggedInUsername(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired(), verify_loggedin_username_validator], render_kw={"class": "verify-username-form-ctl", "autocomplete": "off"})         

     


# Custom validator for security question 1
def question_one_validator(form, field):
    username = session.get('verified_username')

    # Query database for user_id
    user_id = g.db.execute("SELECT id FROM users WHERE user_name = ?", username)
    id = user_id[0]['id']
    #print(id)
   
    # Access user input to question
    title = field.data

    # Verify user input to security question
    favourite_movie = g.db.execute("SELECT movie_title FROM favourites WHERE LOWER(movie_title) = LOWER(?) AND user_id = ?", title, id)

    if not favourite_movie:
        raise ValidationError("Wrong answer, try again")


# Custom validator for security question 2
def question_two_validator(form, field):
    username = session.get('verified_username')

    # Query database for user_id
    user_id = g.db.execute("SELECT id FROM users WHERE user_name = ?", username)
    id = user_id[0]['id']
    #print(id)
   
    # Access user input to question
    title = field.data

    # Verify user input to security question
    watched_movie = g.db.execute("SELECT movie_title FROM watched WHERE LOWER(movie_title) = LOWER(?) AND user_id = ?", title, id)

    if not watched_movie:
        raise ValidationError("Wrong answer, try again")    


# Custom validator for security question 3
def question_three_validator(form, field):
    username = session.get('verified_username')

    # Query database for user_id
    user_id = g.db.execute("SELECT id FROM users WHERE user_name = ?", username)
    id = user_id[0]['id']
    #print(id)

   
    # Access user input to question
    buddy_name = field.data

    # Verify buddy_name
    buddy_name_exists = g.db.execute("SELECT id FROM users WHERE user_name = ?", buddy_name)

    if buddy_name_exists:
        buddy_id = buddy_name_exists[0]['id']

        # Verify user input to security question
        movie_buddy = g.db.execute("SELECT * FROM movie_buddies WHERE (buddy_request_sender = ? AND buddy_request_recipient = ?) AND buddy_status = ? UNION SELECT * FROM movie_buddies WHERE (buddy_request_sender = ? AND buddy_request_recipient = ?) AND buddy_status = ?", id, buddy_id, "Movie Buddies", buddy_id, id, "Movie Buddies" )
    
        if not movie_buddy:
            raise ValidationError("Not your movie buddy, try again")    
    else:
        raise ValidationError("Invalid buddy_name, this user doesnt exist")
        

# Security questions Form
class SecurityQuestions(FlaskForm):
    question_one = StringField('Qn.1 Enter one of your Favourite movies', validators=[InputRequired(), question_one_validator], render_kw={"class": "verify-acc-form-ctl", "autocomplete": "off"})
    question_two = StringField('Qn.2 Enter one of the movies you have Watched', validators=[InputRequired(), question_two_validator], render_kw={"class": "verify-acc-form-ctl", "autocomplete": "off"})
    question_three = StringField('Qn.3 Enter the user name of one of your movie buddies', validators=[InputRequired(), question_three_validator], render_kw={"class": "verify-acc-form-ctl", "autocomplete": "off"}) 


# New password Form
class PasswordReset(FlaskForm):
    new_password = PasswordField('New Password', validators=[InputRequired(), EqualTo('verify_newpassword', message="Passwords do no match"), Length(min=8, message='Password must be atleast 8 characters long'), password_validator], render_kw={"class": "update-password-form-ctl", "id": "new-password"})
    verify_newpassword = PasswordField('Verify New Password', validators=[InputRequired(message='Please repeat the new password')], render_kw={"class": "update-password-form-ctl"})












