from djongo import models
from bson import ObjectId 

class Product(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId) 
    name = models.CharField(max_length=255)
    description = models.TextField()
    price=models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self.name
