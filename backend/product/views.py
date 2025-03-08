from .models import Product
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .models import Product
from .serializers import ProductSerializer

def error(message,status=400):
    return JsonResponse({"error":message},status=status)


products=[]


@api_view(['POST'])
def createProduct(request):
    data = request.data
    print(data)
    serializer = ProductSerializer(data=data)  
    if serializer.is_valid():
        product = serializer.validated_data  
        product["id"]=len(products)+1
        products.append(product)
        return Response( 
            {"message": "Product created", "product": product},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','PATCH'])
def updateProduct(request,product_id):
    if request.method == 'PUT':
        if 0 < product_id <= len(products):  
            data=request.data
            serializer=ProductSerializer(data=data)
            if serializer.is_valid():
                product=serializer.validated_data
                products[product_id - 1].update(product)
                return Response( 
                    {"message": "Product created", "product": product},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    else:
        if 0 < product_id <= len(products):  
            data=request.data
            serializer=ProductSerializer(data=data,partial=True)
            if serializer.is_valid():
                product=serializer.validated_data
                products[product_id - 1].update(product)
                return Response( 
                    {"message": "Product created", "product": product},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteProduct(request, product_id):
    if 0 < product_id <= len(products): 
        deleted_product = products.pop(product_id - 1) 
        for i in range(len(products)):
            products[i]["id"] = i + 1  
        return Response(
            {"message": "Product deleted", "deleted_product": deleted_product},
            status=status.HTTP_200_OK
            )
    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_by_id(request,product_id):
    if 0 < product_id <= len(products):
        return Response(products[product_id-1])
    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_products(request):
    try:
        page=request.GET.get('page',1)
        page_size=3
        paginator=Paginator(products,page_size)
    
        serializer = ProductSerializer(paginator.page(page),many= True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({
           'status':False,
           'message':'invalid page' 
        })
        
# This below is CRUD API without Django-Rest-Framework

        
# @csrf_exempt
# def createProduct(request):
#   if request.method == "POST":
#       data = json.loads(request.body)
#       data["id"] =len(products)+1
#       products.append(data)
#       return JsonResponse({
#           "message": "Product created",
#           "product": data,
#           "products":products
#           }, status=201)
#   return error("Invalid request",400)


# def get_by_id(request,product_id):
#     if request.method == "GET":  
#         if 0 < product_id <= len(products):
#             return JsonResponse(products[product_id-1])
#         return JsonResponse({"error": "Product not found"}, status=404)
#     return error("Invalid request")


# def list_products(request):
#     page_number=request.Get.get("page",1)
#     page_size=request.GET.get("page_size",2)
    
#     paginator=Paginator(products,page_size)
#     try:
#         page=paginator.page(page_number)
#     except:
#         return JsonResponse({"error": "Invalid page number"}, status=400)
    
#     print(page)
#     return JsonResponse({
#         "products": list(page.object_list),
#         "total_pages":paginator.num_pages,
#         "page":page_number
#         })
   

# @csrf_exempt 
# def updateProduct(request,product_id):
#     if request.method=="PUT":
#         if 0 < product_id <= len(products):
#             data=json.loads(request.body)
#             products[product_id - 1].update(data)

#             return JsonResponse({
#                 "message": "Product updated successfully",
#                 "product": products[product_id - 1]
#             }, status=200)
#         return JsonResponse({"error": "Product not found"}, status=404)
#     return error("Invalid request", 400)


# @csrf_exempt
# def deleteProduct(request, product_id):
#     if request.method == "DELETE":
#         if 0 < product_id <= len(products): 
#             deleted_product = products.pop(product_id - 1)
            
#             return JsonResponse({
#                 "message": "Product deleted successfully",
#                 "deleted_product": deleted_product
#             }, status=200)

#         return JsonResponse({"error": "Product not found"}, status=404)
#     return error("Invalid request", 400)
