import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import ProductCategory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_test")


class ProductCategoryAPITest(APITestCase):
   
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mongoengine.disconnect() 
        mongoengine.connect(
            db="test_db",
            alias="default", 
            host="mongodb://root:example@localhost:27019/test_db?authSource=admin",
            username="root",
            password="example",
            authentication_source="admin",
        )

        mongoengine.connect(
            db="test_db",
            alias="test_db_alias",
            host="mongodb://root:example@localhost:27019/test_db?authSource=admin",
            username="root",
            password="example",
            authentication_source="admin",
        )

    @classmethod
    def tearDownClass(cls):
        mongoengine.disconnect(alias="test_db_alias")
        super().tearDownClass()

    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass

    def test_create_category(self):
        url = reverse('product:create_category') 
        data = {
            "title": "Sports",
            "description": "Good Company"
        }
        check_category= ProductCategory.objects.using("test_db_alias").filter(title="Sports").first()
        if not check_category:
            response = self.client.post(url, data, format='json')
            category = ProductCategory.objects.using("test_db_alias").filter(title="Sports").first()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNotNone(category)

    
    def test_update_category(self):
        category = ProductCategory.objects.using("test_db_alias").filter(title="Sports").first()
        if category:
            url = reverse('product:update_category', kwargs={'obj_id': str(category.id)})
            data = { "description": "Best Company"}
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        category = ProductCategory.objects.using("test_db_alias").filter(title="Sports").first()
        if category:
            url=reverse('product:delete_category',kwargs={'obj_id':str(category.id)})
            response=self.client.delete(url)
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            category = ProductCategory.objects.using("test_db_alias").filter(title="Sports").first()
            self.assertIsNone(category)
    
    def test_list_products(self):
        url = reverse('product:list_category') + "?page=1&recent=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)
        self.assertGreaterEqual(len(response.data["categories"]), 0)
