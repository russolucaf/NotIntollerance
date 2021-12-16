from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import EmailField
from wtforms import StringField
from wtforms import SubmitField


class RestaurantForm(FlaskForm):
    partita_iva = StringField(label="Partita Iva")
    name = StringField(label="Nome")
    address = StringField(label="Via")
    civic_number = StringField(label="Numero Civico")
    cap = StringField(label="Cap")
    city = StringField(label="Citta")
    email = EmailField(label="Email")
    url_img = StringField(label="URL Foto")
    number_phone = StringField(label="Numero")
