from django.urls import path
from . import views
from .controllers import productController
from .controllers import categoryController
from .controllers import brandController

app_name='product'

urlpatterns = [
   #Product Paths
   path('',productController.list_products,name='list_products'),
   path('create_product/',productController.createProduct,name='create_product'),
   path('<str:product_id>',productController.get_by_id,name='get_by_id'),
   path('update_product/<str:product_id>',productController.updateProduct,name='update_product'),
   path('delete_product/<str:product_id>',productController.deleteProduct,name='delete_product'),
   path('discount/',productController.apply_discount,name='apply_discount'),
   path('product_from_category_name/<str:title>',productController.product_from_category_name,name='product_from_category_name'),
   
   #Category Path
   path('create_category/',categoryController.createCategory,name='create_category'),
   path('update_category/<str:category_id>',categoryController.updateCategory,name='update_category'),
   path('delete_category/<str:category_id>',categoryController.deleteCategory,name='delete_category'),
   path('list_category/',categoryController.list_category,name='list_category'),
   
   #Brand Path
   path('create_brand/',brandController.createBrand,name='create_brand'),
   path('update_brand/<str:brand_id>',brandController.updateBrand,name='update_brand'),
   path('delete_brand/<str:brand_id>',brandController.deleteBrand,name='delete_brand'),
   path('list_brand/',brandController.list_brand,name='list_brand')
]
