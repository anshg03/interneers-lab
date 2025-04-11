import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import ProductCategory
from mongoengine.context_managers import switch_db
from bson import ObjectId

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

    def test_create_category_when_not_exists(self):
        url = reverse('product:create_category') 
        data = {
            "title": "Sports",
            "description": "Good Company"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        with switch_db(ProductCategory, "test_db_alias") as Category:
            existing = Category.objects(title="Sports").first()
            self.assertIsNotNone(existing)

    def test_create_category_when_exists(self):
        with switch_db(ProductCategory,"test_db_alias") as Category:
            category=Category(title="TestCategory", description="Good Company").save()
            
        url = reverse('product:create_category')
        data = {
            "title": "TestCategory",
            "description": "Good Company"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        with switch_db(ProductCategory, "test_db_alias") as Category:
            Category.objects(id=category.id).delete()
            
    def test_update_category_success(self):
        with switch_db(ProductCategory, "test_db_alias") as Category:
            category = Category(title="UpdateCategory", description="Old Description").save()

        url = reverse('product:update_category', kwargs={'obj_id': str(category.id)})
        data = {"description": "Updated Description"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with switch_db(ProductCategory, "test_db_alias") as Category:
            updated = Category.objects(id=category.id).first()
            self.assertEqual(updated.description, "Updated Description")
            Category.objects(id=category.id).delete()
    
    def test_update_category_failure(self):
        non_existent_id = str(ObjectId())
        url = reverse('product:update_category', kwargs={'obj_id': non_existent_id})
        data = {"description": "New Desc"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with switch_db(ProductCategory, "test_db_alias") as Category:
            category = Category(title="InvalidUpdate", description="Desc").save()

        url = reverse('product:update_category', kwargs={'obj_id': str(category.id)})
        invalid_data = {"title": ""} 
        response = self.client.patch(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with switch_db(ProductCategory, "test_db_alias") as Category:
            Category.objects(id=category.id).delete()        
            
    def test_delete_category_success(self):
        with switch_db(ProductCategory, "test_db_alias") as Category:
            category = Category.objects(title="Sports").first()
            url = reverse('product:delete_category', kwargs={'obj_id': str(category.id)})
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            
            deleted = Category.objects(id=category.id).first()
            self.assertIsNone(deleted)
            
    def test_delete_category_failure(self):
        non_existent_id = str(ObjectId())
        url = reverse('product:delete_category', kwargs={'obj_id': non_existent_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_list_products(self):
        url = reverse('product:list_category') + "?page=1&recent=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)
        self.assertGreaterEqual(len(response.data["categories"]), 0)
