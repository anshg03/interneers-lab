import mongoengine
from product.models import ProductCategory,Product
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

category_data = [
    {"title": "Electronics", "description": "Electronic gadgets and accessories"},
    {"title": "Books", "description": "Books, magazines, and etc"},
    {"title": "Home Appliances", "description": "Appliances for home use"},
]


def seed_categories():
    for category in category_data:
        existing_category = ProductCategory.objects(title=category["title"]).first()
        if not existing_category:
            ProductCategory(**category).save()
            logger.info(f"Category- {category['title']} is created")
        else:
            logger.info(f"Category already exist")
            
def create_default_category():
    default_category,created=ProductCategory.objects.get_or_create(
        title="uncategorized",
        description="assigning categories without category"
    )
    if created:
        logger.info("Created default category Uncategorized")
    return default_category
    
def migrate_existing_category():
    products_without_category = Product.objects(category=None)
    
    if products_without_category.count()>0:
        default_category=create_default_category()
        for product in products_without_category:
            product.category=default_category
            product.save()
        logger.info("Migration completed successfully")
    else:
        logger.info("No Migration needed")
    
    
if __name__=="__main__":
    mongoengine.connect("interneers_lab_mongodb")
    seed_categories()
    migrate_existing_category()
    