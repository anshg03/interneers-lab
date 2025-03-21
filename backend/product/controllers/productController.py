from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.productServices import ProductService 
from product.controllers.baseCRUDController import BaseCRUDView


class ProductView(BaseCRUDView):
    service=ProductService
    function_mapping = {
        "create": "create_product",
        "retrieve": "get_product",
        "update": "update_product",
        "delete": "delete_product",
        "list": "list_products",
    }
    
# class ProductCreateView(APIView):
#     def post(self, request):
#         data = request.data
#         response, status_code = ProductService.create_product(data)
#         return Response(response, status=status_code)

# class ProductUpdateView(APIView):
#     def put(self, request, product_id):
#         data = request.data
#         response, status_code = ProductService.update_product(request, data, product_id)
#         return Response(response, status=status_code)

#     def patch(self, request, product_id):
#         data = request.data
#         response, status_code = ProductService.update_product(request, data, product_id)
#         return Response(response, status=status_code)

# class ProductDeleteView(APIView):
#     def delete(self, request, product_id):
#         response, status_code = ProductService.delete_product(product_id)
#         return Response(response, status=status_code)

# class ProductDetailView(APIView):
#     def get(self, request, product_id):
#         response, status_code = ProductService.get_product(product_id)
#         return Response(response, status=status_code)

# class ProductListView(APIView):
#     def get(self, request):
#         response, status_code = ProductService.list_products(request)
#         return Response(response, status=status_code)

class ProductDiscountView(APIView):
    def post(self, request):
        response, status_code = ProductService.apply_discount(request)
        return Response(response, status=status_code)

class ProductCategoryView(APIView):
    def get(self, request, title):
        response, status_code = ProductService.get_products_by_category(request, title)
        return Response(response, status=status_code)
