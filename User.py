import mongoengine as me


class User(me.Document):
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True, min_length=8, max_length=20)
