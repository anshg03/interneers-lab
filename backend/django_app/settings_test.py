from .settings import * 


MONGODB_DATABASES = {
    "default": {
        "NAME": "test_db",
        "ALIAS": "test_db_alias",
        "HOST": "mongodb://root:example@localhost:27019/test_db?authSource=admin",
        "USERNAME": "root",
        "PASSWORD": "example",
        "AUTHENTICATION_SOURCE": "admin",
    }
}

# Prevent Django from expecting an SQL database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.dummy"  
    }
}

DEBUG=True