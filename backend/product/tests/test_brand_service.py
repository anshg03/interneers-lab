import unittest
from unittest.mock import patch, MagicMock
from product.services.brandServices import BrandService
from product.utils.exceptions import InvalidDataException, NotFoundException


class TestBrandService(unittest.TestCase):

    @patch("product.repository.brandRepository.BrandRepository.create_brand")
    @patch("product.repository.categoryRepository.CategoryRepository.get_by_name")
    @patch("product.serializers.BrandSerializer.is_valid", return_value=True)
    @patch("product.serializers.BrandSerializer.validated_data", new_callable=MagicMock)
    @patch("product.serializers.BrandSerializer.data", new_callable=MagicMock)
    def test_create_brand(self, mock_serialized_data, mock_validated_data, mock_is_valid, mock_get_category, mock_create_brand):
        mock_category = MagicMock(id="catX")
        mock_get_category.return_value = mock_category
        mock_create_brand.return_value = mock_serialized_data
        data = {"name": "Apple", "category": "Electronics"}

        response = BrandService.create_brand(data)

        self.assertEqual(response, mock_serialized_data)
        mock_get_category.assert_called_once_with("Electronics")
        mock_create_brand.assert_called_once_with(mock_validated_data)

    @patch("product.repository.categoryRepository.CategoryRepository.get_by_name", return_value=None)
    def test_create_brand_invalid_category(self, mock_get_category):
        data = {"name": "Apple", "category": "NonExistentCategory"}

        with self.assertRaises(InvalidDataException):
            BrandService.create_brand(data)

    @patch("product.repository.brandRepository.BrandRepository.get_id")
    def test_update_brand_not_found(self, mock_get_id):
        mock_get_id.return_value = None
        with self.assertRaises(NotFoundException):
            BrandService.update_brand(check=True, data={}, brand_id="invalid_id")

    @patch("product.repository.brandRepository.BrandRepository.get_id")
    @patch("product.serializers.BrandSerializer.is_valid", return_value=True)
    @patch("product.serializers.BrandSerializer.validated_data", new_callable=MagicMock)
    @patch("product.repository.brandRepository.BrandRepository.update_brand")
    @patch("product.serializers.BrandSerializer.data", new_callable=MagicMock)
    def test_update_brand(self, mock_serialized_data, mock_update_brand, mock_validated_data, mock_is_valid, mock_get_id):
        mock_brand = MagicMock(id="brandX")
        mock_get_id.return_value = mock_brand
        mock_update_brand.return_value = mock_serialized_data
        data = {"name": "Samsung"}

        response = BrandService.update_brand(check=True, data=data, brand_id="valid_id")

        self.assertEqual(response, mock_serialized_data)
        mock_update_brand.assert_called_once_with(mock_brand, mock_validated_data)

    @patch("product.repository.brandRepository.BrandRepository.get_id")
    @patch("product.repository.brandRepository.BrandRepository.delete_brand")
    def test_delete_brand(self, mock_delete_brand, mock_get_id):
        mock_brand = MagicMock()
        mock_get_id.return_value = mock_brand

        BrandService.delete_brand("valid_id")

        mock_delete_brand.assert_called_once_with(mock_brand)

    @patch("product.repository.brandRepository.BrandRepository.get_id", return_value=None)
    def test_delete_brand_not_found(self, mock_get_id):
        with self.assertRaises(NotFoundException):
            BrandService.delete_brand("invalid_id")

    @patch("product.repository.brandRepository.BrandRepository.get_all")
    @patch("product.serializers.BrandSerializer")
    @patch("django.core.paginator.Paginator.page")
    def test_list_brand(self, mock_paginator_page, mock_serializer, mock_get_all):
        mock_brands = [MagicMock(), MagicMock(), MagicMock()]
        mock_get_all.return_value = mock_brands
        mock_paginator_page.return_value = mock_brands
        mock_serializer.return_value.data = [{"id": "1"}, {"id": "2"}, {"id": "3"}]

        result = BrandService.list_brand({}, page=1, recent=3)

        self.assertTrue(result["status"])
        self.assertEqual(len(result["brands"]), 3)
        mock_get_all.assert_called_once()


if __name__ == "__main__":
    unittest.main()
