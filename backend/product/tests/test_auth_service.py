import unittest
from unittest.mock import patch, MagicMock
from product.services.authServices import AuthService
from product.utils.exceptions import InvalidDataException,AuthException


class TestAuthService(unittest.TestCase):
    
    @patch("product.services.authServices.AuthRepository.create_user")
    @patch("product.services.authServices.AuthRepository.get_user_by_username")
    @patch("product.services.authServices.hash_password")
    @patch("product.services.authServices.UserSignupSerializer", autospec=True)
    def test_create_user_when_not_exists(
        self,
        mock_serializer_class,
        mock_hash_password,
        mock_get_user_by_username,
        mock_create_user
    ):
    
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = {
            "username": "testuser",
            "password": "testpass"
        }
        mock_serializer_class.return_value = mock_serializer_instance

        
        mock_get_user_by_username.return_value = None
        mock_hash_password.return_value = "hashed_password"

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_create_user.return_value = mock_user

        
        response = AuthService.signup_user({"username": "testuser", "password": "testpass"})

        self.assertEqual(response["message"], "User created successfully")
        self.assertEqual(response["username"], "testuser")
        mock_create_user.assert_called_once_with("testuser", "hashed_password")


    @patch("product.services.authServices.AuthRepository.get_user_by_username")   
    @patch("product.services.authServices.hash_password")
    @patch("product.services.authServices.UserSignupSerializer", autospec=True)
    def test_create_user_when_exists(self,mock_serializer_class, mock_hash_password,mock_get_user_by_username,):
        
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = {
            "username": "testuser",
            "password": "testpass"
        }
        mock_serializer_class.return_value = mock_serializer_instance

        
        mock_get_user_by_username.return_value = MagicMock()
        
        with self.assertRaises(AuthException):
            AuthService.signup_user({"username": "testuser", "password": "testpass"})
       
    @patch("product.services.authServices.generate_jwt_token")
    @patch("product.services.authServices.check_password")
    @patch("product.services.authServices.AuthRepository.get_user_by_username")
    @patch("product.services.authServices.UserLoginSerializer", autospec=True)
    def test_login_with_success(
        self,
        mock_serializer_class,
        mock_get_user_by_username,
        mock_check_password,
        mock_generate_jwt_token,
    ): 
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = {
            "username": "testuser",
            "password": "testpass"
        }
        mock_serializer_class.return_value = mock_serializer_instance
        
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.id = "abc123"
        mock_user.password = "hashedpass"
        mock_get_user_by_username.return_value = mock_user
        
        mock_check_password.return_value = True
        mock_generate_jwt_token.return_value = "mocked.jwt.token"
        
        response = AuthService.login_user({"username": "testuser", "password": "testpass"})
        
        self.assertEqual(response, {
            "token": "mocked.jwt.token",
            "username": "testuser"
        })
    
    @patch("product.services.authServices.check_password")
    @patch("product.services.authServices.AuthRepository.get_user_by_username")
    @patch("product.services.authServices.UserLoginSerializer", autospec=True)
    def test_login_with_wrong_password(
        self,
        mock_serializer_class,
        mock_get_user_by_username,
        mock_check_password
    ):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = {
            "username": "testuser",
            "password": "wrongpass"
        }
        mock_serializer_class.return_value = mock_serializer_instance
        
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.password = "correct_hashed_password"
        mock_get_user_by_username.return_value = mock_user
        
        mock_check_password.return_value = False
        
        with self.assertRaises(AuthException) as context:
            AuthService.login_user({"username": "testuser", "password": "wrongpass"})
            
        self.assertEqual(str(context.exception), "Invalid password")