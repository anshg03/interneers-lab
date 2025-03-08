from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
