import mongoengine as me


class Review(me.Document):
    def __init__(self, user_email, restaurant_email, body, *args, **values):
        super().__init__(*args, **values)
        self.user_email = user_email
        self.restaurant_email = restaurant_email
        self.body = body

    user_email = me.StringField(required=True)
    restaurant_email = me.StringField(required=True)
    body = me.StringField(required=True)
