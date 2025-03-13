from .models import Product
from django.http import JsonResponse
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .models import Product
from .serializers import ProductSerializer


@api_view(['POST'])
def createProduct(request):
    data=request.data
    serializer=ProductSerializer(data=data)
    print(serializer)
    if serializer.is_valid():
        product = serializer.save() #in dcument form
        serialized_product = ProductSerializer(product).data #query to json  
        return Response(
            {"message": "Product created", "product": serialized_product},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
def updateProduct(request,product_id):
    data=request.data
    try:
        product=Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    print(product)
    serializer=ProductSerializer(product,data=data,partial=(request.method == 'PATCH'))
    print(serializer)
    if serializer.is_valid():
        updated_product = serializer.save()
        return Response( 
            {"message": "Product updated", "product": ProductSerializer(updated_product).data},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProduct(request,product_id):
    try:
        product=Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response({"message":"Product deleted successfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_by_id(request,product_id):
    try:
        product=Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serialized_product = ProductSerializer(product).data
    return Response(serialized_product, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_products(request):
     products=Product.objects.all()
     page=request.GET.get('page',1)
     page_size=3
     paginator=Paginator(products,page_size)
     
     try:
        paginated_products=paginator.page(page)
        serializer=ProductSerializer(paginated_products,many=True) 
        return Response({
            "status": True,
            "total_pages": paginator.num_pages,
            "current_page": int(page),
            "products": serializer.data
        }, status=status.HTTP_200_OK)
        
     except PageNotAnInteger:
        return Response({
            "status": False,
            "message": "Invalid page number"
        }, status=status.HTTP_400_BAD_REQUEST)

     except EmptyPage:
        return Response({
            "status": False,
            "message": "Page number out of range"
        }, status=status.HTTP_404_NOT_FOUND)
        
#_________________________________________________________________________________

#This is CRUD API using in memory for Products using Django-Rest-Framework(serializers and validator)

# products = []

# @api_view(['POST'])
# def createProduct(request):
#     """
#     Handles the creation of a new product.

#     This function processes a POST request to add a new product to the in-memory `products` list.
#     The request must contain JSON data that represents a product. The product is assigned an
#     incremental ID and then added to the list.All the feilds of Product model are validated using
#     ModelSerializer and Validate function.

#     Args:
#         request: An HttpRequest instance containing the JSON payload of the product.

#     Returns:
#         - If the product is successfully created, returns a JSON response with:
#           - A success message.
#           - The newly added product.
#           - HTTP status 201 (Created).
#         - If the provided data is invalid, returns a JSON response with:
#           - The validation errors.
#           - HTTP status 400 (Bad Request).
#     """
#     data = request.data
#     serializer = ProductSerializer(data=data)  
#     if serializer.is_valid():
#         product = serializer.validated_data  
#         product["id"] = len(products) + 1
#         products.append(product) 
#         return Response(
#             {"message": "Product created", "product": product},
#             status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT', 'PATCH'])
# def updateProduct(request, product_id):
#     """
#     Handles updating an existing product.

#     This function processes a PUT or PATCH request to update a product in the `products` list.
#     All the feilds of Product model are validated using ModelSerializer and Validate function.
#     - PUT replaces all fields of the product.
#     - PATCH updates only the provided fields.

#     Args:
#         request: An HttpRequest instance containing the JSON payload of the updated product data.
#         product_id: The ID of the product to be updated.

#     Returns:
#         - If the product exists and is successfully updated, returns:
#           - A success message.
#           - The updated product.
#           - HTTP status 200 (OK).
#         - If the provided data is invalid, returns:
#           - The validation errors.
#           - HTTP status 400 (Bad Request).
#         - If the product does not exist, returns:
#           - An error message.
#           - HTTP status 404 (Not Found).
#     """
#     if 0 < product_id <= len(products):
#         data = request.data
#         serializer = ProductSerializer(data=data, partial=(request.method == 'PATCH'))
#         if serializer.is_valid():
#             product = serializer.validated_data
#             products[product_id - 1].update(product)
#             return Response(
#                 {"message": "Product updated", "product": product},
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['DELETE'])
# def deleteProduct(request, product_id):
#     """
#     Handles deletion of a product.

#     This function processes a DELETE request to remove a product from the `products` list
#     based on the given product ID.

#     Args:
#         request: An HttpRequest instance.
#         product_id: The ID of the product to be deleted.

#     Returns:
#         - If the product exists and is successfully deleted, returns:
#           - A success message.
#           - The deleted product details.
#           - HTTP status 200 (OK).
#         - If the product does not exist, returns:
#           - An error message.
#           - HTTP status 404 (Not Found).
    
#     Additionally, after deletion, the function reassigns IDs to maintain a continuous sequence.
#     """
#     if 0 < product_id <= len(products):
#         deleted_product = products.pop(product_id - 1) 
#         for i in range(len(products)):
#             products[i]["id"] = i + 1
#         return Response(
#             {"message": "Product deleted", "deleted_product": deleted_product},
#             status=status.HTTP_200_OK
#         )
#     return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def get_by_id(request, product_id):
#     """
#     Retrieves a product by its ID.

#     This function processes a GET request to fetch the details of a product from the `products` list.

#     Args:
#         request: An HttpRequest instance.
#         product_id: The ID of the product to retrieve.

#     Returns:
#         - If the product exists, returns:
#           - The product details.
#           - HTTP status 200 (OK).
#         - If the product does not exist, returns:
#           - An error message.
#           - HTTP status 404 (Not Found).
#     """
#     if 0 < product_id <= len(products):
#         return Response(products[product_id - 1])  
#     return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def list_products(request):
#     """
#     Retrieves a paginated list of products.

#     This function processes a GET request to fetch a paginated list of products from the `products` list,
#     through page query parameter.
    
#     Args:
#         request: An HttpRequest instance that may contain a 'page' query parameter or defaults to 1.

#     Returns:
#         - If the page is valid, returns:
#           - A list of products on the requested page.
#           - HTTP status 200 (OK).
#         - If the requested page is invalid, returns:
#           - An error message.
#           - HTTP status 400 (Bad Request).
    
#     The function uses Django's `Paginator` to handle pagination with a fixed `page_size` manually being added.
#     """
#     try:
#         page = request.GET.get('page', 1) 
#         page_size = 3
#         paginator = Paginator(products, page_size) 

#         serializer = ProductSerializer(paginator.page(page), many=True)
#         return Response(serializer.data)

#     except Exception:
#         return Response({
#             'status': False,
#             'message': 'Invalid page'
#         }, status=status.HTTP_400_BAD_REQUEST)

#__________________________________________________________________________


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
