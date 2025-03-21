from rest_framework.views import APIView
from rest_framework.response import Response

class BaseCRUDView(APIView):
    service = None  
    function_mapping = {}  

    def get(self, request, obj_id=None):
        if obj_id:
            response, status_code = getattr(self.service, self.function_mapping["retrieve"])(obj_id)
        else:
            response, status_code = getattr(self.service, self.function_mapping["list"])(request)
        return Response(response, status=status_code)

    def post(self, request):
        data = request.data
        response, status_code = getattr(self.service, self.function_mapping["create"])(data)
        return Response(response, status=status_code)

    def put(self, request, obj_id):
        data = request.data
        response, status_code = getattr(self.service, self.function_mapping["update"])(request, data, obj_id)
        return Response(response, status=status_code)

    def patch(self, request, obj_id):
        data = request.data
        response, status_code = getattr(self.service, self.function_mapping["update"])(request, data, obj_id)
        return Response(response, status=status_code)

    def delete(self, request, obj_id):
        response, status_code = getattr(self.service, self.function_mapping["delete"])(obj_id)
        return Response(response, status=status_code)
