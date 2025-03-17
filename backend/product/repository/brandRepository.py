from product.models import ProductBrand 
from bson import ObjectId

def createBrand(validated_data):
    brand = ProductBrand(**validated_data)
    brand.save()
    return brand


def getId(brand_id):
    try:
        return ProductBrand.objects.get(id=ObjectId(brand_id))
    except ProductBrand.DoesNotExist:
        return None
    
def updateBrand(brand,validated_data):
    for key,value in validated_data.items():
        setattr(brand,key,value)   
    brand.save()
    return brand

def getAll():
    return ProductBrand.objects.all()

def deleteProduct(brand):
    return brand.delete()

def getByName(name):
    try:   
        return ProductBrand.objects.get(name=name)
    except ProductBrand.DoesNotExist:
        return None
    