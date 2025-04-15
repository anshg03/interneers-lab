from product.repository.authRepository import AuthRepository
from product.utils.hashing import hash_password, check_password
from product.utils.jwt import generate_jwt_token
from product.serializers import UserSignupSerializer, UserLoginSerializer
from product.utils.exceptions import AuthException,InvalidDataException
from typing import Dict,Any

class AuthService:
    
    @staticmethod
    def signup_user(data:Dict[str,Any]) ->Dict[str,Any]:
        serializer = UserSignupSerializer(data=data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            existing_user = AuthRepository.get_user_by_username(username)
            if existing_user:
                raise AuthException("Username already exists")

            hashed = hash_password(password)
            user = AuthRepository.create_user(username, hashed)

            return {
                "message": "User created successfully",
                "username": user.username
            }
        raise InvalidDataException(serializer.errors)


    @staticmethod
    def login_user(data:Dict[str,Any]) -> Dict[str,Any]:
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = AuthRepository.get_user_by_username(username)
            if not user:
                raise AuthException("Invalid username")

            if not check_password(password, user.password):
                raise AuthException("Invalid password")

            token = generate_jwt_token(user.id)

            return {
                "token": token,
                "username": user.username
            }
        raise InvalidDataException(serializer.errors)
