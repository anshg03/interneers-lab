from mongoengine import Document,StringField,IntField,DateTimeField,ReferenceField,CASCADE
from datetime import datetime, timezone


class ProductCategory(Document):
    title=StringField(max_length=255,unique=True)
    description=StringField()
    
    def __str__(self):
        return self.title

class ProductBrand(Document):
    category=ReferenceField(ProductCategory,required=True,reverse_delete_rule=CASCADE)
    name=StringField()
    
    def __str__(self):
        return self.name
    

class Product(Document):
    name = StringField(max_length=255)
    description = StringField()
    price = IntField()
    category = ReferenceField(ProductCategory,required=True,reverse_delete_rule=CASCADE)
    brand = ReferenceField(ProductBrand,required=True,reverse_delete_rule=CASCADE)
    quantity = IntField()
    initial_quantity=IntField(editable=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {
        "collection": "products",
        "indexes": [
            {
                "fields": ["name", "category", "brand"],
                "unique": True
            }
        ]
    }
    def __str__(self):
        return self.name
