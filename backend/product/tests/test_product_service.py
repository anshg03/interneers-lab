import unittest
from unittest.mock import patch, MagicMock
from product.services.productServices import ProductService
from product.utils.exceptions import InvalidDataException, NotFoundException

class TestProductService(unittest.TestCase):
    
    @patch("product.repository.productRepository.ProductRepository.create_product")
    @patch("product.repository.categoryRepository.CategoryRepository.get_by_name")
    @patch("product.repository.brandRepository.BrandRepository.get_by_name")
    @patch("product.serializers.ProductSerializer.is_valid", return_value=True)
    @patch("product.serializers.ProductSerializer.validated_data", new_callable=MagicMock)
    @patch("product.serializers.ProductSerializer.data", new_callable=MagicMock)
    def test_create_product(self,mock_serialized_data,mock_validated_data,mock_is_valid,mock_get_brand,mock_get_category,mock_create_product):
        mock_category=MagicMock(id="catX")
        mock_brand=MagicMock(id="brandX")
        mock_get_category.return_value=mock_category
        mock_get_brand.return_value=mock_brand
        mock_create_product.return_value=mock_serialized_data
        
        data={"name":"Ipad","description":"Best purchase in market","price":30000,"category":"Electronics","brand":"Apple","quantity":500}
        response=ProductService.create_product(data)
    
        self.assertEqual(response, mock_serialized_data)
        mock_get_category.assert_called_once_with("Electronics")
        mock_get_brand.assert_called_once_with("Apple")
        mock_create_product.assert_called_once_with(mock_validated_data)
    
    @patch("product.repository.categoryRepository.CategoryRepository.get_by_name",return_value=None)
    def test_create_product_invalid_category(self,mock_get_category):
        data = {"name": "iPhone", "category": "NonExistentCategory", "brand": "Apple", "price": 1000}
        
        with self.assertRaises(NotFoundException):
            ProductService.create_product(data)
    
    @patch("product.repository.productRepository.ProductRepository.get_id")
    def test_update_product_not_found(self, mock_get_id):
        mock_get_id.return_value = None
        with self.assertRaises(NotFoundException):
            ProductService.update_product(check=True, data={}, product_id="invalid_id")
    
    @patch("product.repository.productRepository.ProductRepository.get_id")     
    @patch("product.repository.productRepository.ProductRepository.update_product")
    @patch("product.repository.categoryRepository.CategoryRepository.get_by_name")
    @patch("product.repository.brandRepository.BrandRepository.get_by_name")
    @patch("product.serializers.ProductSerializer.is_valid", return_value=True)
    @patch("product.serializers.ProductSerializer.validated_data", new_callable=MagicMock)
    @patch("product.serializers.ProductSerializer.data", new_callable=MagicMock)
    def test_update_product(self,mock_serialized_data,mock_validated_data,mock_is_valid,mock_get_brand,mock_get_category,mock_update_product,mock_get_id):
        mock_category=MagicMock(id="catX")
        mock_brand=MagicMock(id="brandX")
        mock_product=MagicMock(id="productX")
        
        mock_get_brand.return_value=mock_brand
        mock_get_category.return_value=mock_category
        mock_get_id.return_value=mock_product
        mock_update_product.return_value=mock_serialized_data
        
        data={"name":"Iphone"}
        
        response=ProductService.update_product(check=True,data=data,product_id="valid_id")
        
        self.assertEqual(response,mock_serialized_data)
        mock_update_product.assert_called_once_with(mock_product, mock_validated_data)
        
    @patch("product.repository.productRepository.ProductRepository.get_id")
    @patch("product.repository.productRepository.ProductRepository.delete_product")
    def test_delete_product(self, mock_delete_product, mock_get_id):
        mock_product = MagicMock(id="productX")
        mock_get_id.return_value = mock_product

        ProductService.delete_product("valid_id")

        mock_delete_product.assert_called_once_with(mock_product)

    @patch("product.repository.productRepository.ProductRepository.get_id", return_value=None)
    def test_delete_product_not_found(self, mock_get_id):
        with self.assertRaises(NotFoundException):
            ProductService.delete_product("invalid_id")
            
            
    @patch("product.repository.productRepository.ProductRepository.get_all")
    @patch("product.repository.productRepository.ProductRepository.filtered_by_recent")
    @patch("django.core.paginator.Paginator.page")
    def test_list_products(self,mock_paginator_page,mock_filtered_recent,mock_get_all):
        mock_products=[MagicMock(), MagicMock(), MagicMock()]
        mock_get_all.return_value=mock_products
        mock_paginator_page.return_value=mock_products
        mock_filtered_recent.return_value=mock_products
        
        response=ProductService.list_products({},page=1,recent=3)
        
        self.assertTrue(response["status"])
        self.assertEqual(len(response["products"]),3)
        mock_get_all.assert_called_once()
    
    @patch("product.repository.productRepository.ProductRepository.product_from_category_name") 
    @patch("product.serializers.ProductSerializer.data", new_callable=MagicMock)
    def test_list_product_by_category(self,mock_serialized_data,mock_products_by_category):
       products_by_category=[MagicMock(), MagicMock()]
       mock_products_by_category.return_value=products_by_category
       
       data={"name":"Electronics"}
       response=ProductService.get_products_by_category(data["name"])
       self.assertEqual(len(response),2)
       mock_products_by_category.assert_called_once()
       
if __name__ == "__main__":
    unittest.main()
        
        