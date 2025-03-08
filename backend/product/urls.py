from django.urls import path
from . import views

app_name='product'

urlpatterns = [
   path('',views.list_products,name='list_products'),
   path('create',views.createProduct,name='createProduct'),
   path('<int:product_id>',views.get_by_id,name='get_by_id'),
   path('update/<int:product_id>',views.updateProduct,name='updateProduct'),
   path('delete/<int:product_id>',views.deleteProduct,name='deleteProduct')
]
