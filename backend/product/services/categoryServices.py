from ..serializers import CategorySerializer
from product.repository.categoryRepository import CategoryRepository
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class CategoryService:
    
    @staticmethod
    def create_category(data):
        serializer=CategorySerializer(data=data)
        if serializer.is_valid():
            category=CategoryRepository.create_category(serializer.validated_data)
            serialized_category=CategorySerializer(category).data
            return {"message": "Category created", "category": serialized_category}, status.HTTP_201_CREATED  
        return serializer.errors, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_category(request,data,category_id):
        category=CategoryRepository.get_id(category_id)
        
        if category==None:
            return {"error":"Category not found"},status.HTTP_400_BAD_REQUEST
        
        serializer=CategorySerializer(category,data=data,partial=(request.method == 'PATCH'))
        
        if serializer.is_valid():
            category=CategoryRepository.update_category(category,serializer.validated_data)
            serialized_category=CategorySerializer(category).data
            return {"message": "Category updated", "category": serialized_category}, status.HTTP_200_OK
        return serializer.errors, status.HTTP_400_BAD_REQUEST
        
    @staticmethod
    def delete_category(category_id):
        category=CategoryRepository.get_id(category_id)
        if category == None:
            return {"error":"Category not found"},status.HTTP_400_BAD_REQUEST
        
        CategoryRepository.delete_category(category)
        return {"message":"Category deleted Succefully"},status.HTTP_200_OK

    @staticmethod
    def list_category(request):
        page=request.GET.get('page',1)
        categorys=CategoryRepository.get_all()
        print(categorys)
        page_size=3
        
        paginator=Paginator(categorys,page_size)
        
        try:
            paginated_categorys=paginator.page(page)
            serializer=CategorySerializer(paginated_categorys,many=True)
            
            return {"status": True,"total_pages": paginator.num_pages,"current_page": int(page),"categorys": serializer.data},status.HTTP_200_OK
        
        except PageNotAnInteger:
            return {"status": False,"message": "Invalid page number"},status.HTTP_400_BAD_REQUEST
        
        except EmptyPage:
            return {"status": False,"message": "Page number out of range"},status.HTTP_404_NOT_FOUND
        
    