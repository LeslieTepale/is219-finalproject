from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class registrationForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired(),])
    password = PasswordField('Password', [validators.DataRequired(),
        validators.length(min=6, max=35)])
    submit = SubmitField()

class loginForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField()

class fileUpload(FlaskForm):
    file = FileField()
    submit = SubmitField()