from typing import Dict, Any, List
from ..serializers import ProductSerializer
from ..repository.productRepository import ProductRepository
from ..repository.categoryRepository import CategoryRepository
from ..repository.brandRepository import BrandRepository
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timezone, timedelta
from product.utils.exceptions import NotFoundException, InvalidDataException

class ProductService:

    @staticmethod
    def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
        category = CategoryRepository.get_by_name(data["category"])
        if not category:
            raise NotFoundException("Invalid category. Category does not exist")
        data["category"] = str(category.id)

        brand = BrandRepository.get_by_name(data["brand"])
        if not brand:
            raise NotFoundException("Invalid brand. Brand does not exist")
        data["brand"] = str(brand.id)

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = ProductRepository.create_product(serializer.validated_data)
            serialized_product = ProductSerializer(product).data
            return serialized_product
        raise InvalidDataException(serializer.errors)

    @staticmethod
    def update_product(check: bool, data: Dict[str, Any], product_id: int) -> Dict[str, Any]:
        product = ProductRepository.get_id(product_id)
        if not product:
            raise NotFoundException("Product not found")

        if "initial_quantity" in data:
            raise InvalidDataException("Updating initial_quantity is not allowed")
        
        if "category" in data:
            category = CategoryRepository.get_by_name(data["category"])
            if not category:
                raise NotFoundException("Invalid category. Category does not exist")
            data["category"] = str(category.id)

        if "brand" in data:
            brand = BrandRepository.get_by_name(data["brand"])
            if not brand:
                raise NotFoundException("Invalid brand. Brand does not exist")
            data["brand"] = str(brand.id)

        if check:
            serializer = ProductSerializer(product, data=data, partial=True)
        else: 
            serializer = ProductSerializer(product, data=data)
            
        if serializer.is_valid():
            updated_product = ProductRepository.update_product(product, serializer.validated_data)
            serialized_product = ProductSerializer(updated_product).data
            return serialized_product
        raise InvalidDataException(serializer.errors)
    
    @staticmethod
    def delete_product(product_id: int) -> None:
        product = ProductRepository.get_id(product_id)
        if not product:
            raise NotFoundException("Product not found")

        ProductRepository.delete_product(product)

    @staticmethod
    def get_product(product_id: int) -> Dict[str, Any]:
        product = ProductRepository.get_id(product_id)
        if not product:
            raise NotFoundException("Product not found")

        serialized_product = ProductSerializer(product).data
        return serialized_product

    @staticmethod
    def list_products(filters: Dict[str, Any], page: int, recent: int) -> Dict[str, Any]:
       
        cleaned_filters={k: v for k, v in filters.items() if v is not None}
        
        if cleaned_filters:
            filtered_products = ProductRepository.filtered_products(cleaned_filters)
        else:
            filtered_products = ProductRepository.get_all() 
            
        filtered_products = ProductRepository.filtered_by_recent(filtered_products, recent)

        page_size = 3
        paginator = Paginator(filtered_products, page_size)

        try:
            paginated_products = paginator.page(page)
            serializer = ProductSerializer(paginated_products, many=True)
            return {
                "status": True,
                "total_pages": paginator.num_pages,
                "current_page": int(page),
                "products": serializer.data
            }

        except PageNotAnInteger:
            raise InvalidDataException("Invalid page number")

        except EmptyPage:
            raise NotFoundException("Page number out of range")


    @staticmethod
    def apply_discount(data: Dict[str, int] ) -> List[Dict[str, Any]]:
        # data = request.data
        # discount_percentage: int = int(data.get("discount", 10))
        discount_percentage=data["discount"]
        apply_time = datetime.now(timezone.utc) - timedelta(minutes=15)
        old_products = ProductRepository.get_old_products(apply_time)

        if not old_products:
            raise NotFoundException("No products eligible for discount.")
 
        products: List[Dict[str, Any]] = []
        for product in old_products:
            initial_price = product.price
            new_cost = initial_price - ((discount_percentage * initial_price) / 100)
            product.price = new_cost
            new_product = ProductRepository.save_product(product)
            products.append(ProductSerializer(new_product).data)

        return products
    
    @staticmethod
    def get_products_by_category(title: str) -> List[Dict[str, Any]]:
        products = ProductRepository.product_from_category_name(title)

        if not products:
             raise NotFoundException("No product exists with such category name")

        serialized_products = ProductSerializer(products, many=True).data
        return serialized_products