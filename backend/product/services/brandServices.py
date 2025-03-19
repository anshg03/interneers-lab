from ..serializers import BrandSerializer
from product.repository.brandRepository import BrandRepository
from product.repository.categoryRepository import CategoryRepository
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class BrandService:
    
    @staticmethod
    def create_brand(data):
        category = CategoryRepository.get_by_name(data["category"]) 
        if category == None:
            return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
        
        data["category"] =str(category.id)
        
        serializer=BrandSerializer(data=data)
        if serializer.is_valid():
            brand=BrandRepository.create_brand(serializer.validated_data)
            serialized_brand=BrandSerializer(brand).data
            return {"message": "Brand created", "Brand": serialized_brand}, status.HTTP_201_CREATED  
        return serializer.errors, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_brand(request,data,brand_id):
        brand=BrandRepository.get_id(brand_id)
        if brand==None:
            return {"error":"Brand not found"},status.HTTP_400_BAD_REQUEST
        
        if "category" in data:
            category = CategoryRepository.get_by_name(data["category"])
            if category == None:
                return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
            data["category"]=str(category.id)
            
        serializer=BrandSerializer(brand,data=data,partial=(request.method == 'PATCH'))
        
        if serializer.is_valid():
            brand=BrandRepository.update_brand(brand,serializer.validated_data)
            serialized_brand=BrandSerializer(brand).data
            return {"message": "Brand updated", "Brand": serialized_brand}, status.HTTP_200_OK
        return serializer.errors, status.HTTP_400_BAD_REQUEST
            

    @staticmethod
    def delete_brand(brand_id):
        brand=BrandRepository.get_id(brand_id)
        if brand == None:
            return {"error":"Brand not found"},status.HTTP_400_BAD_REQUEST
        
        BrandRepository.delete_brand(brand)
        return {"message":"Brand deleted Succefully"},status.HTTP_200_OK

    @staticmethod
    def list_brand(request):
        page=request.GET.get('page',1)
        brands=BrandRepository.get_all()
        page_size=3
        
        paginator=Paginator(brands,page_size)
        
        try:
            paginated_brands=paginator.page(page)
            serializer=BrandSerializer(paginated_brands,many=True)
            
            return {"status": True,"total_pages": paginator.num_pages,"current_page": int(page),"Brands": serializer.data},status.HTTP_200_OK
        
        except PageNotAnInteger:
            return {"status": False,"message": "Invalid page number"},status.HTTP_400_BAD_REQUEST
        
        except EmptyPage:
            return {"status": False,"message": "Page number out of range"},status.HTTP_404_NOT_FOUND
        
        