from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import EmailField


class SignInForm(FlaskForm):
    email = EmailField(label='Email')
    password = PasswordField(label='Password')
