from django.apps import AppConfig
import threading
from product.seed import seed_categories, migrate_existing_category
import logging

logger = logging.getLogger(__name__)

class productConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    
    def ready(self):
        def run_startup_tasks():
            logger.info("Starting category seeding...")
            seed_categories()
            logger.info("Category seeding completed.")

            logger.info("Starting product category migration...")
            migrate_existing_category()
            logger.info("Product category migration completed.")
            
        startup_thread = threading.Thread(target=run_startup_tasks, daemon=True)
        startup_thread.start()