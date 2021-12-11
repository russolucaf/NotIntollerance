import mongoengine as me


class Restaurant(me.Document):
    def __init__(self, partita_iva, name, address, city, email, number_phone, *args, **values):
        super().__init__(*args, **values)
        self.partita_iva = partita_iva
        self.name = name
        self.address = address
        self.city = city
        self.email = email
        self.number_phone = number_phone

    partita_iva = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    address = me.StringField(required=True)
    city = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
    number_phone = me.StringField(required=True)
