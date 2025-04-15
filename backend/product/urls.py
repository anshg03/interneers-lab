from django.urls import path
from .controllers.productController import ProductView, ProductDiscountView, ProductCategoryView
from .controllers.categoryController import CategoryView
from .controllers.brandController import BrandView
from .controllers.authController import SignupView,LoginView

app_name = 'product'

urlpatterns = [
    # Product Paths
    path('', ProductView.as_view(), name='list_products'),
    path('create/', ProductView.as_view(), name='create_product'),
    path('<str:obj_id>/', ProductView.as_view(), name='get_by_id'),
    path('update/<str:obj_id>/', ProductView.as_view(), name='update_product'),
    path('delete/<str:obj_id>/', ProductView.as_view(), name='delete_product'),
    path('discount', ProductDiscountView.as_view(), name='apply_discount'),
    path('product_from_category_name/<str:title>/', ProductCategoryView.as_view(), name='product_from_category_name'),

    # Category Paths
    path('category', CategoryView.as_view(), name='list_category'),
    path('category/create/', CategoryView.as_view(), name='create_category'),
    path('category/update/<str:obj_id>/', CategoryView.as_view(), name='update_category'),
    path('category/delete/<str:obj_id>/', CategoryView.as_view(), name='delete_category'),

    # Brand Paths
    path('brand', BrandView.as_view(), name='list_brand'),
    path('brand/create/', BrandView.as_view(), name='create_brand'),
    path('brand/update/<str:obj_id>/', BrandView.as_view(), name='update_brand'),
    path('brand/delete/<str:obj_id>/', BrandView.as_view(), name='delete_brand'),
    
    #Auth paths
    path('signup',SignupView.as_view(),name="signup"),
    path('login',LoginView.as_view(),name="login")
    
]
