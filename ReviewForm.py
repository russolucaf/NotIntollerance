from wtforms import StringField
from flask_wtf import FlaskForm


class ReviewForm(FlaskForm):
    body = StringField(label='Recensione')
