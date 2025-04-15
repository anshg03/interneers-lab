import os
import mongoengine
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from mongoengine.context_managers import switch_db
from product.models import User
from product.utils.hashing import hash_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_test")

class UserAPITest(APITestCase):

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

    def test_create_user_when_not_exists(self):
        url = reverse("product:signup")
        data = {
            "username": "newuser",
            "password": "securepass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with switch_db(User, "test_db_alias") as user:
            created_user = user.objects(username="newuser").first()
            self.assertIsNotNone(created_user)
        
        with switch_db(User,"test_db_alias") as user:
            user.objects(username="newuser").delete()


    def test_create_user_when_exists(self):
        with switch_db(User, "test_db_alias") as user:
            user(username="existinguser", password="hashedpass").save()

        url = reverse("product:signup")
        data = {
            "username": "existinguser",
            "password": "any_password"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        with switch_db(User, "test_db_alias") as user:
            user.objects(username="existinguser").delete()

    def test_login_with_correct_credentials(self):
        with switch_db(User, "test_db_alias") as user:
            hashed = hash_password("pass123")
            user(username="validuser", password=hashed).save()

        url = reverse("product:login")
        data = {
            "username": "validuser",
            "password": "pass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "validuser")

        with switch_db(User, "test_db_alias") as user:
            user.objects(username="validuser").delete()

    def test_login_with_incorrect_password(self):
        with switch_db(User, "test_db_alias") as user:
            hashed = hash_password("correctpass")
            user(username="passuser", password=hashed).save()

        url = reverse("product:login")
        data = {
            "username": "passuser",
            "password": "wrongpass"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with switch_db(User, "test_db_alias") as user:
            user.objects(username="passuser").delete()