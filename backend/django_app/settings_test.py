from .settings import * 
from mongoengine import connect,disconnect


disconnect(alias='default')

MONGO_DB_NAME = "test_db"
connect(
    db=MONGO_DB_NAME,
    host="mongodb://root:example@localhost:27019/test_db?authSource=admin",
    username="root",
    password="example",
    authentication_source="admin",
)

# Test runner configuration (use Nose for testing)
INSTALLED_APPS += ["django_nose"]
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
