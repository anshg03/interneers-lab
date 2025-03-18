from ..serializers import ProductSerializer
from ..repository import productRepository
from ..repository import categoryRepository,brandRepository
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime,timezone,timedelta 

def createProduct(data):
    category = categoryRepository.getByName(data["category"]) 
    if category == None:
        return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
    data["category"] =str(category.id)
    
    brand=brandRepository.getByName(data["brand"])
    if brand == None:
        return {"error": "Invalid brand. Brand does not exist"}, status.HTTP_400_BAD_REQUEST
    data["brand"]=str(brand.id)
    
    serializer=ProductSerializer(data=data)
    if serializer.is_valid():
        product = productRepository.createProduct(serializer.validated_data)
        serialized_product=ProductSerializer(product).data
        return {"message": "Product created", "product": serialized_product}, status.HTTP_201_CREATED  
    return serializer.errors, status.HTTP_400_BAD_REQUEST


def updateProduct(request,data,product_id):
    product = productRepository.getId(product_id)
    if product == None:
        return {"error": "Product not found"},status.HTTP_400_BAD_REQUEST
    
    if "initial_quantity" in data:
        return {"error":"Updating initial_quantity is not allowed"},status.HTTP_400_BAD_REQUEST
    
    if "category" in data:
        category = categoryRepository.getByName(data["category"])
        if category == None:
            return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
        data["category"]=str(category.id)
        
    if "brand" in data:
        brand=brandRepository.getByName(data["brand"])
        if brand == None:
            return {"error": "Invalid brand. Brand does not exist"}, status.HTTP_400_BAD_REQUEST
        data["brand"]=str(brand.id)
        
    
    serializer=ProductSerializer(product,data=data,partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        updated_product=productRepository.updateProduct(product,serializer.validated_data)
        serialized_product=ProductSerializer(updated_product).data
        return {"message":"Product updated","product":serialized_product},status.HTTP_200_OK
    return serializer.errors,status.HTTP_400_BAD_REQUEST
    

def deleteProduct(product_id):
    product=productRepository.getId(product_id)
    if product == None:
        return {"error":"Product not found"},status.HTTP_400_BAD_REQUEST
    
    productRepository.deleteProduct(product)
    return {"message":"Product Delete Succefully"},status.HTTP_200_OK


def getProduct(product_id):
    product=productRepository.getId(product_id)
    if product == None:
        return {"error":"Product not found"},status.HTTP_400_BAD_REQUEST
    
    serialized_product=ProductSerializer(product).data
    return {"product":serialized_product},status.HTTP_200_OK
       
       
def list_products(request):
    recent = int(request.GET.get("recent", productRepository.getAll().count()))
    
    filters = {}

    if "min_price" in request.GET:
        filters["min_price"] = request.GET["min_price"]
    if "max_price" in request.GET:
        filters["max_price"] = request.GET["max_price"]
    if "brand" in request.GET:
        filters["brand"] = request.GET["brand"]
    if "in_stock" in request.GET:
        filters["in_stock"] = request.GET["in_stock"]

    filtered_products = productRepository.filteredProducts(filters)
    
    filtered_products=productRepository.filteredByRecent(filtered_products,recent)

    page=request.GET.get('page',1)
    page_size=3
    paginator=Paginator(filtered_products,page_size)
    
    try:
        paginated_products=paginator.page(page)
        serializer=ProductSerializer(paginated_products,many=True)
        
        return {"status": True,"total_pages": paginator.num_pages,"current_page": int(page),"products": serializer.data},status.HTTP_200_OK
    
    except PageNotAnInteger:
        return {"status": False,"message": "Invalid page number"},status.HTTP_400_BAD_REQUEST
    
    except EmptyPage:
        return {"status": False,"message": "Page number out of range"},status.HTTP_404_NOT_FOUND
        
    
def apply_discount(request):
    data=request.data
    discount_percentage = int(data.get("discount", 10))
    
    apply_time=datetime.now(timezone.utc)-timedelta(minutes=15)
    
    old_products=productRepository.getOldProducts(apply_time)
    
    if not old_products.exists(): 
        return {"message": "No products eligible for discount."},status.HTTP_200_OK
    
    products=[]
    for product in old_products:
        initial_price=product.price
        new_cost=initial_price-((discount_percentage*initial_price)/100)
        product.price=new_cost
        new_product=productRepository.saveProduct(product)
        products.append(ProductSerializer(new_product).data)
        
    return {
            "message": f"Discount of {discount_percentage}% applied successfully.",
            "products": products
            },status.HTTP_200_OK
 
    
def product_from_category_name(request,title):
    products=productRepository.product_from_category_name(title)
    
    if not products:
        return {"error":"No product exist which such category name"},status.HTTP_400_BAD_REQUEST
    serialized_products = ProductSerializer(products, many=True).data
    
    return {"message":"All the product with this category name","products":serialized_products},status.HTTP_200_OK

    