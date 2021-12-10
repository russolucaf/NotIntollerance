import mongoengine as me


class Restaurant(me.Document):
    partita_iva = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    address = me.StringField(required=True)
    city = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
