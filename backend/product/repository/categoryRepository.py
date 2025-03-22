from typing import Optional, Dict, Any
from django.db.models.query import QuerySet
from product.models import ProductCategory
from bson import ObjectId


class CategoryRepository:
    
    @staticmethod
    def create_category(validated_data: Dict[str, Any]) -> ProductCategory:
        category = ProductCategory(**validated_data)
        category.save()
        return category

    @staticmethod
    def get_id(category_id: str) -> Optional[ProductCategory]:
        try:
            return ProductCategory.objects.get(id=ObjectId(category_id))
        except ProductCategory.DoesNotExist:
            return None

    @staticmethod
    def update_category(category: ProductCategory, validated_data: Dict[str, Any]) -> ProductCategory:
        for key, value in validated_data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def get_all() -> QuerySet[ProductCategory]:  
        return ProductCategory.objects.all()

    @staticmethod
    def delete_category(category: ProductCategory) -> None:
        category.delete()

    @staticmethod
    def get_by_name(title: str) -> Optional[ProductCategory]:
        try:
            return ProductCategory.objects.get(title=title)
        except ProductCategory.DoesNotExist:
            return None
