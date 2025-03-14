from django.urls import path
from . import views
from .controllers import productController

app_name='product'

urlpatterns = [
   path('',productController.list_products,name='list_products'),
   path('create',productController.createProduct,name='createProduct'),
   path('<str:product_id>',productController.get_by_id,name='get_by_id'),
   path('update/<str:product_id>',productController.updateProduct,name='updateProduct'),
   path('delete/<str:product_id>',productController.deleteProduct,name='deleteProduct'),
   path('discount/',productController.apply_discount,name='apply_discount')
]
