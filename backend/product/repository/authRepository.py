from product.models import User 
from mongoengine.context_managers import switch_db
import os
import sys


def get_db_alias() -> str:
    from django.conf import settings
    is_test = (
        os.getenv("TESTING") == "true"
        or "test" in sys.argv
        or getattr(settings, "TESTING", False)
    )
    alias = "test_db_alias" if is_test else "main_db_alias"
    return alias

class AuthRepository:
    
    @staticmethod
    def create_user(username: str, hashed_password: str)->User:
        user = User(username=username, password=hashed_password)
        with switch_db(User,get_db_alias()):
            user.save()
        return user
    
    @staticmethod
    def get_user_by_username(username:str) ->User:
        with switch_db(User, get_db_alias()) as user:
            return user.objects(username=username).first()