from typing import Optional,Dict,Any
from product.models import ProductBrand
from bson import ObjectId
from django.db.models.query import QuerySet


class BrandRepository:
    
    @staticmethod
    def create_brand(validated_data: Dict[str, Any]) -> ProductBrand:
        brand = ProductBrand(**validated_data)
        brand.save()
        return brand

    @staticmethod
    def get_id(brand_id: str) -> Optional[ProductBrand]:
        try:
            return ProductBrand.objects.get(id=ObjectId(brand_id))
        except ProductBrand.DoesNotExist:
            return None
    
    @staticmethod
    def update_brand(brand: ProductBrand, validated_data: Dict[str, Any]) -> ProductBrand:
        for key, value in validated_data.items():
            setattr(brand, key, value)
        brand.save()
        return brand

    @staticmethod
    def get_all() -> QuerySet[ProductBrand]:
        return ProductBrand.objects.all()

    @staticmethod
    def delete_brand(brand: ProductBrand) -> None:
        brand.delete()

    @staticmethod
    def get_by_name(name: str) -> Optional[ProductBrand]:
        try:
            return ProductBrand.objects.get(name=name)
        except ProductBrand.DoesNotExist:
            return None
