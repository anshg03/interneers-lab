from typing import Optional, Dict, Any
from product.models import Product, ProductCategory
from bson import ObjectId
from datetime import datetime, timezone
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
    return alias

class ProductRepository:

    @staticmethod
    def create_product(validated_data: Dict[str, Any]) -> Product:
        product = Product(**validated_data)
        product.initial_quantity = product.quantity
        with switch_db(Product, get_db_alias()):
            product.save()
        return product

    @staticmethod
    def save_product(product: Product) -> Product:
        product.updated_at = datetime.now(timezone.utc)
        with switch_db(Product, get_db_alias()) as ProductCls:
            ProductCls.objects(id=product.id).update(
                set__updated_at=product.updated_at,
                set__price=product.price
            )
        return product

    @staticmethod
    def get_id(product_id: str) -> Optional[Product]:
        with switch_db(Product, get_db_alias()) as ProductCls:
            try:
                return ProductCls.objects.get(id=ObjectId(product_id))
            except Product.DoesNotExist:
                return None

    @staticmethod
    def update_product(product: Product, validated_data: Dict[str, Any]) -> Product:
        for key, value in validated_data.items():
            setattr(product, key, value)
        product.updated_at = datetime.now(timezone.utc)
        with switch_db(Product, get_db_alias()):
            product.save()
        return product

    @staticmethod
    def delete_product(product: Product) -> None:
        with switch_db(Product, get_db_alias()):
            product.delete()

    @staticmethod
    def get_all():
        with switch_db(Product, get_db_alias()) as ProductCls:
            return ProductCls.objects.all()

    @staticmethod
    def filtered_products(filters: Dict[str, Any]):
        query: Dict[str, Any] = {}

        if "min_price" in filters:
            query["price__gte"] = filters["min_price"]
        if "max_price" in filters:
            query["price__lte"] = filters["max_price"]
        if "brand" in filters:
            query["brand"] = filters["brand"]
        if filters.get("in_stock") == "true":
            query["quantity__gt"] = 0
        elif filters.get("in_stock") == "false":
            query["quantity__lte"] = 0

        with switch_db(Product, get_db_alias()) as ProductCls:
            return ProductCls.objects.filter(**query)

    @staticmethod
    def filtered_by_recent(filtered_products, recent: int):
        return filtered_products.order_by("-created_at")[:recent]

    @staticmethod
    def get_old_products(apply_time: datetime):
        with switch_db(Product, get_db_alias()) as ProductCls:
            return ProductCls.objects.filter(
                created_at__lte=apply_time,
                __raw__={"$expr": {"$eq": ["$quantity", "$initial_quantity"]}},
            )

    @staticmethod
    def product_from_category_name(title: str):
        with switch_db(ProductCategory, get_db_alias()) as CategoryCls:
            category = CategoryCls.objects.filter(title=title).first()

        if not category:
            return Product.objects.none()

        with switch_db(Product, get_db_alias()) as ProductCls:
            return ProductCls.objects.filter(category=ObjectId(category.id))
