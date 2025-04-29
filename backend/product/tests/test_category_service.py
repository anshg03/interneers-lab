import unittest
from unittest.mock import patch, MagicMock
from product.services.categoryServices import CategoryService
from product.utils.exceptions import NotFoundException

class TestCategoryService(unittest.TestCase):

    @patch("product.repository.categoryRepository.CategoryRepository.create_category")
    @patch("product.serializers.CategorySerializer.is_valid", return_value=True)
    @patch("product.serializers.CategorySerializer.validated_data", new_callable=MagicMock)
    @patch("product.serializers.CategorySerializer.data", new_callable=MagicMock)
    def test_create_category(self, mock_serialized_data, mock_validated_data, mock_is_valid, mock_create_category):
        mock_create_category.return_value = mock_serialized_data
        data = {"title": "Electronics", "description": "Electronic gadgets and accessories"}
        response = CategoryService.create_category(data , image=None)
        self.assertEqual(response, mock_serialized_data)
        mock_create_category.assert_called_once_with(mock_validated_data)

    @patch("product.repository.categoryRepository.CategoryRepository.get_id")
    def test_update_category_not_found(self, mock_get_id):
        mock_get_id.return_value = None
        with self.assertRaises(NotFoundException):
            CategoryService.update_category(check=True, data={}, category_id="invalid_id")

    @patch("product.repository.categoryRepository.CategoryRepository.get_id")
    @patch("product.serializers.CategorySerializer.is_valid", return_value=True)
    @patch("product.serializers.CategorySerializer.validated_data", new_callable=MagicMock)
    @patch("product.repository.categoryRepository.CategoryRepository.update_category")
    @patch("product.serializers.CategorySerializer.data", new_callable=MagicMock)
    def test_update_category(self, mock_serialized_data, mock_update_category, mock_validated_data, mock_is_valid, mock_get_id):
        mock_get_id.return_value = MagicMock()
        mock_update_category.return_value = mock_serialized_data
        data = {"title": "Updated Electronics", "description": "Electronic gadgets and accessories"}
        response = CategoryService.update_category(check=True, data=data, category_id="valid_id")
        self.assertEqual(response, mock_serialized_data)
        mock_update_category.assert_called_once_with(mock_get_id.return_value,mock_validated_data)

    @patch("product.repository.categoryRepository.CategoryRepository.get_id")
    @patch("product.repository.categoryRepository.CategoryRepository.delete_category")
    def test_delete_category(self, mock_delete_category, mock_get_id):
        mock_get_id.return_value = MagicMock()
        CategoryService.delete_category("valid_id")
        mock_delete_category.assert_called_once()

    @patch("product.repository.categoryRepository.CategoryRepository.get_id")
    def test_delete_category_not_found(self, mock_get_id):
        mock_get_id.return_value = None
        with self.assertRaises(NotFoundException):
            CategoryService.delete_category("invalid_id")

    @patch("product.repository.categoryRepository.CategoryRepository.get_all")
    @patch("product.serializers.CategorySerializer.data", new_callable=MagicMock)
    def test_list_category(self, mock_serialized_data, mock_get_all):
        mock_get_all.return_value = [MagicMock(), MagicMock(), MagicMock()]
        response = CategoryService.list_category(filters={}, page=1, recent=3)
        self.assertTrue(response["status"])
        self.assertIn("categories", response)

if __name__ == "__main__":
    unittest.main()
