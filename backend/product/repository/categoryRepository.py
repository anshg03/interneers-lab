from typing import Optional, Dict, Any
from product.models import ProductCategory
from bson import ObjectId
from mongoengine.context_managers import switch_db
import os
import sys

def get_db_alias() -> str:
    from django.conf import settings
    is_test = (
        os.getenv("TESTING") == "true"
        or "test" in sys.argv
        or getattr(settings, "TESTING", False)
    )
    alias = "test_db_alias" if is_test else "main_db_alias"
    # print(f" Using DB alias: {alias}")
    return alias

class CategoryRepository:

    @staticmethod
    def create_category(validated_data: Dict[str, Any]) -> ProductCategory:
        category = ProductCategory(**validated_data)
        with switch_db(ProductCategory, get_db_alias()):
            category.save()
        return category

    @staticmethod
    def get_id(category_id: str) -> Optional[ProductCategory]:
        with switch_db(ProductCategory, get_db_alias()) as Category:
            return Category.objects(id=ObjectId(category_id)).first()

    @staticmethod
    def update_category(category: ProductCategory, validated_data: Dict[str, Any]) -> ProductCategory:
        for key, value in validated_data.items():
            setattr(category, key, value)
        with switch_db(ProductCategory, get_db_alias()):
            category.save()
        return category

    @staticmethod
    def get_all():
        with switch_db(ProductCategory, get_db_alias()) as Category:
            return Category.objects.all()

    @staticmethod
    def delete_category(category: ProductCategory) -> None:
        with switch_db(ProductCategory, get_db_alias()):
            category.delete()

    @staticmethod
    def get_by_name(title: str) -> Optional[ProductCategory]:
        with switch_db(ProductCategory, get_db_alias()) as Category:
            return Category.objects(title=title).first()
