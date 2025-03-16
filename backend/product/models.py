from mongoengine import Document, StringField, IntField,DateTimeField,ReferenceField,CASCADE
from datetime import datetime, timezone


class ProductCategory(Document):
    title=StringField(max_length=255)
    description=StringField()
    
    def __str__(self):
        return self.title


class Product(Document):
    name = StringField(max_length=255)
    description = StringField()
    price = IntField()
    category = ReferenceField(ProductCategory,required=True,reverse_delete_rule=CASCADE)
    brand = StringField(max_length=100)
    quantity = IntField()
    initial_quantity=IntField(editable=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {"collection": "products"} 

    def __str__(self):
        return self.name
