from product.models import Product
from bson import ObjectId
from datetime import datetime,timezone

def createProduct(validated_data):
    product = Product(**validated_data)
    product.initial_quantity=product.quantity
    product.save()
    return product

def saveProduct(product):
    product.updated_at=datetime.now(timezone.utc)
    Product.objects(id=product.id).update(set__updated_at=product.updated_at, set__price=product.price)
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
    
    product.updated_at=datetime.now(timezone.utc)
    product.save()
    return product

def deleteProduct(product):
    product.delete()
    
def getAll():
    return Product.objects.all()

def filteredProducts(filters):
    query= {}
    
    if "min_price" in filters:
        query["price__gte"]=filters["min_price"]
    if "max_price" in filters:
        query["price__lte"] = filters["max_price"]
    if "brand" in filters:
        query["brand"] = filters["brand"]
    if filters["in_stock"] == "true":
        query["quantity__gt"] = 0  
    elif filters["in_stock"] == "false":
        query["quantity__lte"] = 0
    
    return Product.objects.filter(**query)  


def filteredByRecent(filtered_products,recent):
    return filtered_products.order_by('-created_at')[:recent]
    
           
def getOldProducts(apply_time):
    return Product.objects.filter(
    created_at__lte=apply_time,
    __raw__={"$expr": {"$eq": ["$quantity", "$initial_quantity"]}}
    )

def product_from_category_name(title):
    return Product.objects.filter(category__title=title)
