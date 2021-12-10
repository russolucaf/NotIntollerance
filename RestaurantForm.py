from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import EmailField
from wtforms import StringField
from wtforms import SubmitField


class RestaurantForm(FlaskForm):
    name = StringField(label="Partita iva")
    position = StringField(label="Via")
    email = EmailField(label="Email")
