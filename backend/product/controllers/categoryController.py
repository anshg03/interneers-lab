from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.categoryServices import CategoryService  

class CategoryCreateView(APIView):
    def post(self, request):
        data = request.data
        response, status_code = CategoryService.create_category(data)
        return Response(response, status=status_code)


class CategoryUpdateView(APIView):
    def put(self, request, category_id):
        data = request.data
        response, status_code = CategoryService.update_category(request, data, category_id)
        return Response(response, status=status_code)

    def patch(self, request, category_id):
        data = request.data
        response, status_code = CategoryService.update_category(request, data, category_id)
        return Response(response, status=status_code)


class CategoryDeleteView(APIView):
    def delete(self, request, category_id):
        response, status_code = CategoryService.delete_category(category_id)
        return Response(response, status=status_code)


class CategoryListView(APIView):
    def get(self, request):
        response, status_code = CategoryService.list_category(request)
        return Response(response, status=status_code)
