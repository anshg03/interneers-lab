from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services import productServices


@api_view(['POST'])
def createProduct(request):
    data=request.data
    response,status_code =productServices.createProduct(data)
    return Response(response, status=status_code)

@api_view(['PUT','PATCH'])
def updateProduct(request,product_id):
    data=request.data
    response,status_code=productServices.updateProduct(request,data,product_id)
    return Response(response,status=status_code)

@api_view(['DELETE'])
def deleteProduct(request,product_id):
    response,status_code=productServices.deleteProduct(product_id)
    return Response(response,status=status_code)
 
@api_view(['GET'])
def get_by_id(request,product_id):
    response,status_code=productServices.getProduct(product_id)
    return Response(response,status=status_code)

@api_view(['GET'])
def list_products(request):
    response,status_code=productServices.list_products(request)
    return Response(response,status=status_code)

@api_view(['POST'])
def apply_discount(request):
    response,status_code=productServices.apply_discount(request)
    return Response(response,status=status_code)


@api_view(['GET'])
def product_from_category_name(request,title):
    response,status_code=productServices.product_from_category_name(request,title)
    return Response(response,status=status_code)


