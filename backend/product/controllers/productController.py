from typing import Dict,Type
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from ..services.productServices import ProductService 
from product.controllers.baseCRUDController import BaseCRUDView
from product.utils.exceptions import NotFoundException,InvalidDataException

class ProductView(BaseCRUDView):
    service: Type[ProductService]=ProductService
    function_mapping : Dict[str,str]= {
        "create": "create_product",
        "retrieve": "get_product",
        "update": "update_product",
        "delete": "delete_product",
        "list": "list_products",
    }

class ProductDiscountView(APIView):
    def post(self, request: Request) -> Response:
        
        try:
            response = ProductService.apply_discount(request.data)
            return Response(response, status=status.HTTP_200_OK)
        except NotFoundException as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidDataException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ProductCategoryView(APIView):
    def get(self, request: Request, title: str) -> Response:
        
        try:
            response = ProductService.get_products_by_category(title)
            return Response(response, status=status.HTTP_200_OK)
        except NotFoundException as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
