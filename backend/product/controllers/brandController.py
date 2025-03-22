from rest_framework.views import APIView
from typing import Dict,Type
from rest_framework.response import Response
from ..services.brandServices import BrandService
from product.controllers.baseCRUDController import BaseCRUDView


class BrandView(BaseCRUDView):
    service: Type[BrandService]=BrandService
    function_mapping : Dict[str,str]= {
        "create": "create_brand",
        "update": "update_brand",
        "delete": "delete_brand",
        "list": "list_brand",   
    }
    