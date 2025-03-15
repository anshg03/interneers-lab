from ..serializers import CategorySerializer
from product.repository import categoryRepository
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def createCategory(data):
    serializer=CategorySerializer(data=data)
    if serializer.is_valid():
        category=categoryRepository.createCategory(serializer.validated_data)
        serialized_category=CategorySerializer(category).data
        return {"message": "Category created", "category": serialized_category}, status.HTTP_201_CREATED  
    return serializer.errors, status.HTTP_400_BAD_REQUEST


def updateCategory(request,data,category_id):
    category=categoryRepository.getId(category_id)
    
    if category==None:
        return {"error":"Category not found"},status.HTTP_400_BAD_REQUEST
    
    serializer=CategorySerializer(category,data=data,partial=(request.method == 'PATCH'))
    
    if serializer.is_valid():
        category=categoryRepository.updateCategory(category,serializer.validated_data)
        serialized_category=CategorySerializer(category).data
        return {"message": "Category updated", "category": serialized_category}, status.HTTP_200_OK
    return serializer.errors, status.HTTP_400_BAD_REQUEST
        

def deleteCategory(category_id):
    category=categoryRepository.getId(category_id)
    if category == None:
        return {"error":"Category not found"},status.HTTP_400_BAD_REQUEST
    
    categoryRepository.deleteProduct(category)
    return {"message":"Category deleted Succefully"},status.HTTP_200_OK

def listCategory(request):
    page=request.GET.get('page',1)
    categorys=categoryRepository.getAll()
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
    
    