import mongoengine
import os
from product.models import ProductBrand, ProductCategory, Product
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings_test")

mongoengine.disconnect(alias="default")

ProductCategory._meta["db_alias"] = "test_db_alias"
ProductBrand._meta["db_alias"] = "test_db_alias"
Product._meta["db_alias"] = "test_db_alias"

mongoengine.connect(
    db="test_db",
    alias="test_db_alias", 
    host="mongodb://root:example@localhost:27019/test_db?authSource=admin",
    username="root",
    password="example",
    authentication_source="admin",
)

def seed_data():
    category = ProductCategory.objects.using("test_db_alias").first()
    if not category:
        category = ProductCategory(title="Electronics", description="Good product")
        category.save(using="test_db_alias")
        logger.info("Test DB: Category inserted: Electronics")

    brand = ProductBrand.objects.using("test_db_alias").first()
    if not brand:
        brand = ProductBrand(name="Apple", category=category)
        brand.save(using="test_db_alias")
        logger.info("Test DB: Brand inserted: Apple")

    if not Product.objects.using("test_db_alias").first():
        Product(
            name="iPhone 15",
            description="Good product",
            category=category,
            brand=brand,
            price=1200,
            quantity=10
        ).save(using="test_db_alias")
        logger.info("Test DB: Product inserted: iPhone 15")

        Product(
            name="MacBook Pro",
            description="Good product",
            category=category,
            brand=brand,
            price=2500,
            quantity=5
        ).save(using="test_db_alias")
        logger.info("Test DB: Product inserted: MacBook Pro")

    logger.info("Test DB: Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()
