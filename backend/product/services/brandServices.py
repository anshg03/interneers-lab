from typing import Any, Dict
from ..serializers import BrandSerializer
from product.repository.brandRepository import BrandRepository
from product.repository.categoryRepository import CategoryRepository
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from product.utils.exceptions import NotFoundException, InvalidDataException

class BrandService:
    
    @staticmethod
    def create_brand(data: Dict[str, Any], image:None) -> Dict[str, Any]:
        category = CategoryRepository.get_by_name(data["category"]) 
        if category is None:
            raise InvalidDataException("Invalid category. Category does not exist")
        
        data["category"] = str(category.id)
        
        if image:
            from cloudinary.uploader import upload
            uploaded = upload(image)
            data["image_url"] = uploaded.get("secure_url")
        
        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            brand = BrandRepository.create_brand(serializer.validated_data)
            serialized_brand = BrandSerializer(brand).data
            return serialized_brand  
        raise InvalidDataException(serializer.errors)

    @staticmethod
    def update_brand(check: bool, data: Dict[str, Any], brand_id: str) -> Dict[str, Any]:
        brand = BrandRepository.get_id(brand_id)
        if brand is None:
            raise NotFoundException("Brand not found")
        
        if "category" in data:
            category = CategoryRepository.get_by_name(data["category"])
            if category is None:
                raise InvalidDataException("Invalid category. Category does not exist")
            data["category"] = str(category.id)
            
        if check:    
            serializer = BrandSerializer(brand, data=data, partial=True)
        else :
           serializer = BrandSerializer(brand, data=data) 
        
        if serializer.is_valid():
            brand = BrandRepository.update_brand(brand, serializer.validated_data)
            serialized_brand = BrandSerializer(brand).data
            return  serialized_brand
        raise InvalidDataException(serializer.errors)
            

    @staticmethod
    def delete_brand(brand_id: str) -> None:
        brand = BrandRepository.get_id(brand_id)
        if brand is None:
            raise NotFoundException("Brand not found")
        
        BrandRepository.delete_brand(brand)

    @staticmethod
    def list_brand(filters: Dict[str, Any], page: int, recent: int) -> Dict[str, Any]:
        
        brands = BrandRepository.get_all()
        page_size: int = 3

        paginator = Paginator(brands, page_size)

        try:
            paginated_brands = paginator.page(page)
            serializer = BrandSerializer(paginated_brands, many=True)

            return {
                "status": True,
                "total_pages": paginator.num_pages,
                "current_page": int(page),
                "brands": serializer.data,
            }

        except PageNotAnInteger:
            raise InvalidDataException("Invalid page number")

        except EmptyPage:
            raise NotFoundException("Page number out of range")
