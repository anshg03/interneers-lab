from typing import Optional, Dict, Any
from product.models import ProductBrand
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

class BrandRepository:

    @staticmethod
    def create_brand(validated_data: Dict[str, Any]) -> ProductBrand:
        brand = ProductBrand(**validated_data)
        with switch_db(ProductBrand, get_db_alias()):
            brand.save()
        return brand

    @staticmethod
    def get_id(brand_id: str) -> Optional[ProductBrand]:
        with switch_db(ProductBrand, get_db_alias()) as Brand:
            return Brand.objects(id=ObjectId(brand_id)).first()

    @staticmethod
    def update_brand(brand: ProductBrand, validated_data: Dict[str, Any]) -> ProductBrand:
        for key, value in validated_data.items():
            setattr(brand, key, value)
        with switch_db(ProductBrand, get_db_alias()):
            brand.save()
        return brand

    @staticmethod
    def get_all():
        with switch_db(ProductBrand, get_db_alias()) as Brand:
            return Brand.objects.all()

    @staticmethod
    def delete_brand(brand: ProductBrand) -> None:
        with switch_db(ProductBrand, get_db_alias()):
            brand.delete()

    @staticmethod
    def get_by_name(name: str) -> Optional[ProductBrand]:
        with switch_db(ProductBrand, get_db_alias()) as Brand:
            return Brand.objects(name=name).first()
