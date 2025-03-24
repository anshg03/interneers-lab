from typing import Optional, Dict, Any
from django.db.models.query import QuerySet
from product.models import Product, ProductCategory
from bson import ObjectId
from datetime import datetime, timezone


class ProductRepository:

    @staticmethod
    def create_product(validated_data: Dict[str, Any]) -> Product:
        product = Product(**validated_data)
        product.initial_quantity = product.quantity
        product.save()
        return product

    @staticmethod
    def save_product(product: Product) -> Product:
        product.updated_at = datetime.now(timezone.utc)
        Product.objects(id=product.id).update(
            set__updated_at=product.updated_at, set__price=product.price
        )
        return product

    @staticmethod
    def get_id(product_id: str) -> Optional[Product]:
        try:
            return Product.objects.get(id=ObjectId(product_id))
        except Product.DoesNotExist:
            return None

    @staticmethod
    def update_product(product: Product, validated_data: Dict[str, Any]) -> Product:
        for key, value in validated_data.items():
            setattr(product, key, value)

        product.updated_at = datetime.now(timezone.utc)
        product.save()
        return product

    @staticmethod
    def delete_product(product: Product) -> None:
        product.delete()

    @staticmethod
    def get_all() -> QuerySet[Product]: 
        return Product.objects.all()

    @staticmethod
    def filtered_products(filters: Dict[str, Any]) -> QuerySet[Product]: 
        query: Dict[str, Any] = {}

        if "min_price" in filters:
            query["price__gte"] = filters["min_price"]
        if "max_price" in filters:
            query["price__lte"] = filters["max_price"]
        if "brand" in filters:
            query["brand"] = filters["brand"]
        if filters["in_stock"] == "true":
            query["quantity__gt"] = 0
        elif filters["in_stock"] == "false":
            query["quantity__lte"] = 0

        return Product.objects.filter(**query)

    @staticmethod
    def filtered_by_recent(filtered_products: QuerySet[Product], recent: int) -> QuerySet[Product]: 
        return filtered_products.order_by("-created_at")[:recent]

    @staticmethod
    def get_old_products(apply_time: datetime) -> QuerySet[Product]: 
        return Product.objects.filter(
            created_at__lte=apply_time,
            __raw__={"$expr": {"$eq": ["$quantity", "$initial_quantity"]}},
        )

    @staticmethod
    def product_from_category_name(title: str) -> QuerySet[Product]: 
        category = ProductCategory.objects.filter(title=title).first()

        if not category:
            return []

        return Product.objects.filter(category=ObjectId(category.id))
