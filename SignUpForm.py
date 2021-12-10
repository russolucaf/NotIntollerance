from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import SubmitField


class SignUp(FlaskForm):
    name = StringField(label='Nome')
    surname = StringField(label='Cognome')
    email = StringField(label='Email')
    password = PasswordField(label='Password')