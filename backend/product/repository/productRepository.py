from product.models import Product
from bson import ObjectId


def createProduct(validated_data):
    product = Product(**validated_data)
    product.save()
    return product

def getId(product_id):
    try:
        return Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return None
    
def updateProduct(product,validated_data):
    print(validated_data)
    for key,value in validated_data.items():
        setattr(product,key,value)
    print(product)
    product.save()
    return product

def deleteProduct(product):
    product.delete()
    
def getAll():
    return Product.objects.all()