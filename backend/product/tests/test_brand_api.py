import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from mongoengine.context_managers import switch_db
from product.models import ProductBrand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_test")

class ProductBrandAPITest(APITestCase):
   
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

    def test_create_brand(self):
        url = reverse('product:create_brand') 
        data = {
            "name": "Greenply",
            "category": "Home Appliances"
        }

        with switch_db(ProductBrand, "test_db_alias") as Brand:
            existing = Brand.objects(name="Greenply").first()
            if not existing:
                response = self.client.post(url, data, format='json')
                brand = Brand.objects(name="Greenply").first()
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIsNotNone(brand)

    def test_update_brand(self):
        with switch_db(ProductBrand, "test_db_alias") as Brand:
            brand = Brand.objects(name="Greenply").first()
            if brand:
                url = reverse('product:update_brand', kwargs={'obj_id': str(brand.id)})
                data = {"name": "Greenply"}
                response = self.client.patch(url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_brand(self):
        with switch_db(ProductBrand, "test_db_alias") as Brand:
            brand = Brand.objects(name="Greenply").first()
            if brand:
                url = reverse('product:delete_brand', kwargs={'obj_id': str(brand.id)})
                response = self.client.delete(url)
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

                deleted = Brand.objects(id=brand.id).first()
                self.assertIsNone(deleted)

    def test_list_brands(self):
        url = reverse('product:list_brand') + "?page=1&recent=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("brands", response.data)
        self.assertGreaterEqual(len(response.data["brands"]), 0)