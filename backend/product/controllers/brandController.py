from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.brandServices import BrandService
from product.controllers.baseCRUDController import BaseCRUDView


class BrandView(BaseCRUDView):
    service=BrandService
    function_mapping={
        "create": "create_brand",
        "update": "update_brand",
        "delete": "delete_brand",
        "list": "list_brand",   
    }
    
    
# class BrandCreateView(APIView):
#     def post(self, request):
#         data = request.data
#         response, status_code = BrandService.create_brand(data)
#         return Response(response, status=status_code)


# class BrandUpdateView(APIView):
#     def put(self, request, brand_id):
#         data = request.data
#         response, status_code = BrandService.update_brand(request, data, brand_id)
#         return Response(response, status=status_code)

#     def patch(self, request, brand_id):
#         data = request.data
#         response, status_code = BrandService.update_brand(request, data, brand_id)
#         return Response(response, status=status_code)


# class BrandDeleteView(APIView):
#     def delete(self, request, brand_id):
#         response, status_code = BrandService.delete_brand(brand_id)
#         return Response(response, status=status_code)


# class BrandListView(APIView):
#     def get(self, request):
#         response, status_code = BrandService.list_brand(request)
#         return Response(response, status=status_code)
