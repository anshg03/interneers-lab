from typing import Any, Dict, Tuple
from ..serializers import CategorySerializer
from product.repository.categoryRepository import CategoryRepository
from rest_framework import status
from rest_framework.request import Request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from product.exceptions import InvalidDataException,NotFoundException

class CategoryService:

    @staticmethod
    def create_category(data: Dict[str, Any]) -> Dict[str, Any]:
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category = CategoryRepository.create_category(serializer.validated_data)
            serialized_category = CategorySerializer(category).data
            return serialized_category
        raise InvalidDataException(serializer.errors)

    @staticmethod
    def update_category(check:bool, data: Dict[str, Any], category_id: str) -> Dict[str, Any] :
        category = CategoryRepository.get_id(category_id)

        if category is None:
            raise NotFoundException("Category not found")

        if check:
            serializer = CategorySerializer(category, data=data, partial=True)
        else:
            serializer = CategorySerializer(category, data=data)

        if serializer.is_valid():
            category = CategoryRepository.update_category(category, serializer.validated_data)
            serialized_category = CategorySerializer(category).data
            return serialized_category
        raise InvalidDataException(serializer.errors)
    
    @staticmethod
    def delete_category(category_id: str) -> None:
        category = CategoryRepository.get_id(category_id)
        if category is None:
            raise NotFoundException("Category not found")

        CategoryRepository.delete_category(category)

    @staticmethod
    def list_category(filters: Dict[str, Any], page: int, recent: int) -> Dict[str, Any]:
        
        categories = CategoryRepository.get_all()
        page_size: int = 3

        paginator = Paginator(categories, page_size)

        try:
            paginated_categories = paginator.page(page)
            serializer = CategorySerializer(paginated_categories, many=True)

            return {
                "status": True,
                "total_pages": paginator.num_pages,
                "current_page": int(page),
                "categories": serializer.data,
            }

        except PageNotAnInteger:
            raise InvalidDataException("Invalid page number")

        except EmptyPage:
            raise NotFoundException("Page number out of range")

