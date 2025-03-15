from product.models import ProductCategory 
from bson import ObjectId

def createCategory(validated_data):
    category = ProductCategory(**validated_data)
    category.save()
    return category


def getId(category_id):
    try:
        return ProductCategory.objects.get(id=ObjectId(category_id))
    except ProductCategory.DoesNotExist:
        return None
    
def updateCategory(category,validated_data):
    for key,value in validated_data.items():
        setattr(category,key,value)   
    category.save()
    return category

def getAll():
    return ProductCategory.objects.all()

def deleteProduct(category):
    return category.delete()


    