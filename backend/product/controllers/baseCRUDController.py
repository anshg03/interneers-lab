from typing import Dict, Type, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from product.utils.exceptions import NotFoundException, InvalidDataException
from rest_framework import status


class BaseCRUDView(APIView):
    service: Type[Any] = None
    function_mapping: Dict[str, str] = {}

    def handle_request(self, func, *args, success_status=status.HTTP_200_OK, **kwargs) -> Response:
        
        try:
            response= func(*args, **kwargs)
            return Response(response, status=success_status)
        except NotFoundException as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidDataException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request: Request, obj_id: int = None) -> Response:
        if obj_id:
            return self.handle_request(
                getattr(self.service, self.function_mapping["retrieve"]),
                obj_id,
            )
        
        filters = {
            "min_price": request.GET.get("min_price"),
            "max_price": request.GET.get("max_price"),
            "brand": request.GET.get("brand"),
            "in_stock": request.GET.get("in_stock") == "True",
        }
        page = int(request.GET.get("page", 1))
        recent = int(request.GET.get("recent", 10))

        return self.handle_request(
            getattr(self.service, self.function_mapping["list"]),
            filters,
            page,
            recent
        )

    def post(self, request: Request) -> Response:
        return self.handle_request(
            getattr(self.service, self.function_mapping["create"]),
            request.data,
            success_status=status.HTTP_201_CREATED,
        )

    def put(self, request: Request, obj_id: int) -> Response:
        return self.handle_request(
            getattr(self.service, self.function_mapping["update"]),
            False,
            request.data,
            obj_id,
        )
    
    def patch(self, request: Request, obj_id: int) -> Response:
        return self.handle_request(
            getattr(self.service, self.function_mapping["update"]),
            True,
            request.data,
            obj_id,
        )

    def delete(self, request: Request, obj_id: int) -> Response:
        return self.handle_request(
            getattr(self.service, self.function_mapping["delete"]),
            obj_id,
            success_status=status.HTTP_204_NO_CONTENT,
        )
