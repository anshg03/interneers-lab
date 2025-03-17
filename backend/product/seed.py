import mongoengine
from product.models import ProductCategory
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
            
if __name__=="__main__":
    mongoengine.connect("interneers_lab_mongodb")
    seed_categories()