from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import EmailField
from wtforms import StringField
from wtforms import SubmitField


class RestaurantForm(FlaskForm):
    partita_iva = StringField(label="Iva")
    name = StringField(label="Nome")
    address = StringField(label="Via")
    city = StringField(label="Citta")
    email = EmailField(label="Email")
    number_phone = StringField(label="Numero")
