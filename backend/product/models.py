from mongoengine import Document, StringField, IntField

class Product(Document):
    name = StringField(max_length=255)
    description = StringField()
    price = IntField()
    category = StringField(max_length=100)
    brand = StringField(max_length=100)
    quantity = IntField()

    meta = {"collection": "products"} 

    def __str__(self):
        return self.name
