from django.urls import path
from . import views
from .controllers import productController
from .controllers import categoryController

app_name='product'

urlpatterns = [
   #Product Paths
   path('',productController.list_products,name='list_products'),
   path('create',productController.createProduct,name='createProduct'),
   path('<str:product_id>',productController.get_by_id,name='get_by_id'),
   path('update/<str:product_id>',productController.updateProduct,name='updateProduct'),
   path('delete/<str:product_id>',productController.deleteProduct,name='deleteProduct'),
   path('discount/',productController.apply_discount,name='apply_discount'),
   
   #Category Path
   path('create_category/',categoryController.createCategory,name='create_category'),
   path('update_category/<str:category_id>',categoryController.updateCategory,name='update_category'),
   path('delete_category/<str:category_id>',categoryController.deleteCategory,name='delete_category'),
   path('list_category/',categoryController.list_category,name='list_category')
]
