from rest_framework.views import APIView
from rest_framework.response import Response
from typing import Dict,Type
from ..services.categoryServices import CategoryService  
from product.controllers.baseCRUDController import BaseCRUDView


class CategoryView(BaseCRUDView):
    service : Type[CategoryService]=CategoryService  
    function_mapping : Dict[str,str]= {
        "create": "create_category",
        "update": "update_category",
        "delete": "delete_category",
        "list": "list_category",
    }
    