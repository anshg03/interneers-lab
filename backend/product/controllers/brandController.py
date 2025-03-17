from product.services import brandServices
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def createBrand(request):
    data=request.data
    response,status_code =brandServices.createBrand(data)
    return Response(response, status=status_code)

@api_view(['PUT','PATCH'])
def updateBrand(request,brand_id):
    data=request.data
    response,status_code = brandServices.updateBrand(request,data,brand_id)
    return Response(response,status=status_code)

@api_view(['DELETE'])
def deleteBrand(request,brand_id):
    response,status_code = brandServices.deleteBrand(brand_id)
    return Response(response,status=status_code)

@api_view(['GET'])
def list_brand(request):
    response,status_code = brandServices.listBrand(request)
    return Response(response,status=status_code)