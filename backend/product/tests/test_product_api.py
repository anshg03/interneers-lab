import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import Product
from datetime import datetime, timezone, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_test")


class ProductAPITest(APITestCase):
   
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

    def test_create_product(self):
        url = reverse('product:create_product') 
        data = {
            "name": "iPhone",
            "description": "Good product",
            "category": "Electronics",
            "brand": "Apple",
            "price": 9999,
            "quantity": 300
        }
        check_product= Product.objects.using("test_db_alias").filter(name="iPhone").first()
        if not check_product:
            response = self.client.post(url, data, format='json')
            product = Product.objects.using("test_db_alias").filter(name="iPhone").first()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNotNone(product)
            self.assertEqual(product.price, 9999)

    
    def test_update_product(self):
        product = Product.objects.using("test_db_alias").filter(name="iPhone").first()
        if product:
            url = reverse('product:update_product', kwargs={'obj_id': str(product.id)})
            data = {"price": 1799}
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    def test_get_product(self):
        product = Product.objects.using("test_db_alias").filter(name="iPhone").first()
        if product:
            url=reverse('product:get_by_id',kwargs={'obj_id':str(product.id)})
            response=self.client.get(url)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data['name'], "iPhone")

    def test_delete_product(self):
        product = Product.objects.using("test_db_alias").filter(name="iPhone").first()
        if product:
            url=reverse('product:delete_product',kwargs={'obj_id':str(product.id)})
            response=self.client.delete(url)
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            product = Product.objects.using("test_db_alias").filter(name="iPhone").first()
            self.assertIsNone(product)
    
    def test_list_products(self):
        url = reverse('product:list_products') + "?page=1&recent=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertGreaterEqual(len(response.data["products"]), 0)
    
    def test_get_products_by_category(self):
        title="Electronics"
        url=reverse('product:product_from_category_name',kwargs={'title':title})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for product in response.data:
            self.assertEqual(product['category'], title)
            
    def test_apply_discount(self):
        url_discount=reverse('product:apply_discount')
        discount_data={"discount":10} 
        product_data={
            "name":"Old Laptop",
            "description":"Test Product",
            "category":"Electronics",
            "brand":"Apple",
            "price":1000,
            "quantity":5,
        }
        check_product= Product.objects.using("test_db_alias").filter(name="Old Laptop").first()
        if not check_product:
            url_create= reverse('product:create_product') 
            res=self.client.post(url_create,product_data,format='json')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        apply_time = datetime.now(timezone.utc) - timedelta(minutes=16)  
        created_product = Product.objects.using("test_db_alias").filter(name="Old Laptop").first()
        created_product.created_at = apply_time
        created_product.save()

        response=self.client.post(url_discount,discount_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_product = Product.objects.get(id=created_product.id)
        expected_price = created_product.price - ((10 * created_product.price) / 100)
        self.assertEqual(updated_product.price, int(expected_price))