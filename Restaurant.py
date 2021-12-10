import mongoengine as me


class Restaurant(me.Document):
    name = me.StringField(required=True)
    position = me.StringField(required=True)
    email = me.EmailField(required=True)
