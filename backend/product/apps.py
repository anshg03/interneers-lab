from django.apps import AppConfig
import threading
from product.seed import seed_categories


class productConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    
    def ready(self):
        threading.Thread(target=seed_categories).start()
