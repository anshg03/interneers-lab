from ..serializers import BrandSerializer
from product.repository import brandRepository,categoryRepository
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def createBrand(data):
    category = categoryRepository.getByName(data["category"]) 
    if category == None:
        return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
    
    data["category"] =str(category.id)
    
    serializer=BrandSerializer(data=data)
    if serializer.is_valid():
        brand=brandRepository.createBrand(serializer.validated_data)
        serialized_brand=BrandSerializer(brand).data
        return {"message": "Brand created", "Brand": serialized_brand}, status.HTTP_201_CREATED  
    return serializer.errors, status.HTTP_400_BAD_REQUEST


def updateBrand(request,data,brand_id):
    brand=brandRepository.getId(brand_id)
    if brand==None:
        return {"error":"Brand not found"},status.HTTP_400_BAD_REQUEST
    
    if "category" in data:
        category = categoryRepository.getByName(data["category"])
        if category == None:
            return {"error": "Invalid category. Category does not exist"}, status.HTTP_400_BAD_REQUEST
        data["category"]=str(category.id)
        
    serializer=BrandSerializer(brand,data=data,partial=(request.method == 'PATCH'))
    
    if serializer.is_valid():
        brand=brandRepository.updateBrand(brand,serializer.validated_data)
        serialized_brand=BrandSerializer(brand).data
        return {"message": "Brand updated", "Brand": serialized_brand}, status.HTTP_200_OK
    return serializer.errors, status.HTTP_400_BAD_REQUEST
        

def deleteBrand(brand_id):
    brand=brandRepository.getId(brand_id)
    if brand == None:
        return {"error":"Brand not found"},status.HTTP_400_BAD_REQUEST
    
    brandRepository.deleteProduct(brand)
    return {"message":"Brand deleted Succefully"},status.HTTP_200_OK


def listBrand(request):
    page=request.GET.get('page',1)
    brands=brandRepository.getAll()
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
    
    