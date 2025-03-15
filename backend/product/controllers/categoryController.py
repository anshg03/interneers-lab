from product.services import categoryServices
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def createCategory(request):
    data=request.data
    response,status_code=categoryServices.createCategory(data)
    return Response(response, status=status_code)

@api_view(['PUT','PATCH'])
def updateCategory(request,category_id):
    data=request.data
    response,status_code=categoryServices.updateCategory(request,data,category_id)
    return Response(response,status=status_code)

@api_view(['DELETE'])
def deleteCategory(request,category_id):
    response,status_code=categoryServices.deleteCategory(category_id)
    return Response(response,status=status_code)

@api_view(['GET'])
def list_category(request):
    response,status_code=categoryServices.listCategory(request)
    return Response(response,status=status_code)