import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from product.services.productServices import ProductService


class TestProductService(unittest.TestCase):
    
    def setUp(self):
        self.mock_product_repo = patch("product.repository.productRepository.ProductRepository").start()
        self.mock_category_repo = patch("product.repository.categoryRepository.CategoryRepository").start()
        self.mock_brand_repo = patch("product.repository.brandRepository.BrandRepository").start()

        self.addCleanup(patch.stopall)
     
    def test_create_product_success(self):
        mock_category=MagicMock(id="category_id")
        mock_brand=MagicMock(id="brand_id")
        
        self.mock_category_repo.get_by_name.return_value=mock_category
        self.mock_brand_repo.get_by_name.return_value = mock_brand
        
        mock_product = MagicMock(
            id="product_id",
            name="Laptop",
            price=1000,
            quantity=50,
            category="category_id",
            brand="brand_id"
        )

        self.mock_product_repo.create_product.return_value=mock_product
        data={"name":"cake","category":"Food","brand":"Britannia","price":50,"quantity":100}
        response,status_code= ProductService.create_product(data)
        
        self.mock_category_repo.get_by_name.assert_called_once_with("Food")
        self.mock_brand_repo.get_by_name.assert_called_once_with("Britannia")
        self.mock_product_repo.create_product.assert_call_once()
        
        self.assertEqual(status_code,status.HTTP_201_CREATED)
        self.assertIn("product",response)
        
    def test_get_product_success(self):
        mock_product=MagicMock(id="product_id")
        self.mock_product_repo.get_id.return_value=mock_product
        
        response,status_code=ProductService.get_product("product_id")
        
        self.mock_product_repo.get_id.assert_called_once_with("product_id")
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIn("product", response)
        
    def test_update_product__patch_success(self):
        mock_product = MagicMock(
            id="product_id",
            name="cake",
            price=50,
            category="category_id",
            brand="brand_id",
            quantity=100,
            initial_quantity=100
        )
        self.mock_product_repo.get_id.return_value=mock_product
        
        updated_data={"name":"biscuit"}
        self.mock_product_repo.update_product.return_value=mock_product
        
        mock_request=MagicMock(method="PATCH")
        response,status_code=ProductService.update_product("product_id",updated_data,mock_request)
        
        self.mock_product_repo.get_id.assert_called_once_with("product_id")
        self.mock_product_repo.update_product.assert_called_once()
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIn("product", response)
        
    def test_update_product_put_success(self):
        mock_product = MagicMock(
            id="product_id",
            name="cake",
            price=50,
            category="category_id",
            brand="brand_id",
            quantity=100,
            initial_quantity=100
        )
        self.mock_product_repo.get_id.return_value = mock_product

        updated_data = {"name": "biscuit", "price": 50, "quantity": 100, "brand": "Britannia", "category": "Food"}
        self.mock_product_repo.update_product.return_value = mock_product

        mock_request = MagicMock(method="PUT") 
        response, status_code = ProductService.update_product("product_id",updated_data,mock_request)

        self.mock_product_repo.get_id.assert_called_once_with("product_id")
        self.mock_product_repo.update_product.assert_called_once()
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIn("product", response)
        
    def test_delete_product_success(self):
        mock_product = MagicMock(
            id="product_id",
            name="biscuit",
            price=50,
            category="category_id",
            brand="brand_id",
            quantity=100,
            initial_quantity=100
        )
        self.mock_product_repo.get_id.return_value = mock_product

        response, status_code = ProductService.delete_product("product_id")

        self.mock_product_repo.get_id.assert_called_once_with("product_id")
        self.mock_product_repo.delete_product.assert_called_once_with(mock_product)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response, {"message": "Product Deleted Successfully"})
        
