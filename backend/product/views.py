from .models import Product
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def error(message,status=400):
    return JsonResponse({"error":message},status=status)

products=[]

@csrf_exempt
def createProduct(request):
  if request.method == "POST":
      data = json.loads(request.body)
      data["id"] =len(products)+1
      products.append(data)
      return JsonResponse({
          "message": "Product created",
          "product": data,
          "products":products
          }, status=201)
  return error("Invalid request",400)

def get_by_id(request,product_id):
    if request.method == "GET":  
        if 0 < product_id <= len(products):
            return JsonResponse(products[product_id-1])
        return JsonResponse({"error": "Product not found"}, status=404)
    return error("Invalid request")

def list_products(request):
    return JsonResponse({"products": products})
   
@csrf_exempt 
def updateProduct(request,product_id):
    if request.method=="PUT":
        if 0 < product_id <= len(products):
            data=json.loads(request.body)
            products[product_id - 1].update(data)

            return JsonResponse({
                "message": "Product updated successfully",
                "product": products[product_id - 1]
            }, status=200)
        return JsonResponse({"error": "Product not found"}, status=404)
    return error("Invalid request", 400)

@csrf_exempt
def deleteProduct(request, product_id):
    if request.method == "DELETE":
        if 0 < product_id <= len(products): 
            deleted_product = products.pop(product_id - 1)
            
            return JsonResponse({
                "message": "Product deleted successfully",
                "deleted_product": deleted_product
            }, status=200)

        return JsonResponse({"error": "Product not found"}, status=404)
    return error("Invalid request", 400)
