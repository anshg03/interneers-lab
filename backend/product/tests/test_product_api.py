import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import Product,ProductBrand,ProductCategory
from datetime import datetime, timezone, timedelta
from mongoengine.context_managers import switch_db
from bson import ObjectId

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

    def test_create_product_when_not_exists(self):
        url = reverse('product:create_product') 
        data = {
            "name": "iPhone",
            "description": "Good product",
            "category": "Electronics",
            "brand": "Apple",
            "price": 9999,
            "quantity": 300,
            "image_url":"https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
        }
        response = self.client.post(url, data, format='json')
        with switch_db(Product, "test_db_alias") as ProductModel:
            product = ProductModel.objects(name="iPhone").first()
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(product)
        self.assertEqual(product.price, 9999)

    def test_create_product_when_exists(self):
        with switch_db(ProductCategory, "test_db_alias") as Category:
            category = Category.objects(title="Electronics").first()

        with switch_db(ProductBrand, "test_db_alias") as Brand:
            brand = Brand.objects(name="Apple").first()
            
        with switch_db(Product, "test_db_alias") as ProductModel:
            existing_product = ProductModel(
                name="XPS 15",
                description="Premium laptop",
                category=str(category.id),
                brand=str(brand.id),
                price=12000,
                quantity=50,
                initial_quantity=50,
                image_url="https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
            ).save()
            
        url = reverse('product:create_product')
        data = {
            "name": "XPS 15",
            "description": "Premium laptop",
            "category": "Electronics",
            "brand": "Apple",
            "price": 12000,
            "quantity": 50,
            "image_url":"https://cdn.oreillystatic.com/oreilly/images/device-image4-800x600-20210224.jpg"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        with switch_db(Product, "test_db_alias") as ProductModel:
            ProductModel.objects(id=existing_product.id).delete()
    
    def test_update_product_success(self):
        with switch_db(Product, "test_db_alias") as ProductModel:
            product = ProductModel.objects(name="iPhone 15").first()
            self.assertIsNotNone(product)

        url = reverse('product:update_product', kwargs={'obj_id': str(product.id)})
        data = {"price": 1799}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with switch_db(Product, "test_db_alias") as ProductModel:
            updated = ProductModel.objects(id=product.id).first()
            self.assertEqual(updated.price, 1799) 
    
    def test_update_product_failure(self):
        invalid_id = str(ObjectId())
        url = reverse('product:update_product', kwargs={'obj_id': invalid_id})
        data = {"price": 1999}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_product_with_invalid_price(self):
        with switch_db(Product, "test_db_alias") as ProductModel:
            product = ProductModel.objects(name="iPhone 15").first()
            self.assertIsNotNone(product)

        url = reverse('product:update_product', kwargs={'obj_id': str(product.id)})
        data = {"price": -50}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_product_success(self):
        with switch_db(Product, "test_db_alias") as ProductModel:
            product = ProductModel.objects(name="iPhone 15").first()
            self.assertIsNotNone(product)

        url = reverse('product:get_by_id', kwargs={'obj_id': str(product.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "iPhone 15")

    def test_get_product_failure(self):
        invalid_id = str(ObjectId())
        url = reverse('product:get_by_id', kwargs={'obj_id': invalid_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_success(self):
        with switch_db(Product, "test_db_alias") as ProductModel:
            product = ProductModel.objects(name="iPhone").first()
            self.assertIsNotNone(product)

        url = reverse('product:delete_product', kwargs={'obj_id': str(product.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with switch_db(Product, "test_db_alias") as ProductModel:
            deleted = ProductModel.objects(id=product.id).first()
            self.assertIsNone(deleted)
            
    def test_delete_product_failure(self):
        invalid_id = str(ObjectId())
        url = reverse('product:delete_product', kwargs={'obj_id': invalid_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        with switch_db(ProductCategory, "test_db_alias") as CategoryModel:
            category = CategoryModel.objects(title=title).first()
            self.assertIsNotNone(category)

        with switch_db(Product, "test_db_alias") as ProductModel:
            expected_products = ProductModel.objects(category=category.id)
            self.assertEqual(len(response.data), expected_products.count())
            
        for product in response.data:
            self.assertEqual(product['category'], title)
            
    def test_apply_discount_success(self):
        url_discount = reverse('product:apply_discount')
        discount_data = {"discount": 10}
        product_data = {
            "name": "Old Laptop",
            "description": "Test Product",
            "category": "Electronics",
            "brand": "Apple",
            "price": 1000,
            "quantity": 5,
        }

        url_create = reverse('product:create_product')
        res = self.client.post(url_create, product_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        apply_time = datetime.now(timezone.utc) - timedelta(minutes=16)

        with switch_db(Product, "test_db_alias") as ProductModel:
            created_product = ProductModel.objects(name="Old Laptop").first()
            self.assertIsNotNone(created_product)

            created_product.created_at = apply_time
            created_product.save()

        response = self.client.post(url_discount, discount_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with switch_db(Product, "test_db_alias") as ProductModel:
            updated_product = ProductModel.objects(id=created_product.id).first()
            self.assertIsNotNone(updated_product)

            expected_price = created_product.price - ((10 * created_product.price) / 100)
            self.assertEqual(updated_product.price, int(expected_price))
        
        with switch_db(Product, "test_db_alias") as ProductModel:
            ProductModel.objects(id=created_product.id).delete()
        
