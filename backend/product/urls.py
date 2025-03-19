from django.urls import path
from .controllers.productController import (
    ProductCreateView, ProductDeleteView, ProductCategoryView,
    ProductDetailView, ProductDiscountView, ProductListView, ProductUpdateView
)
from .controllers.categoryController import (
    CategoryCreateView, CategoryDeleteView, CategoryListView, CategoryUpdateView
)
from .controllers.brandController import (
    BrandCreateView, BrandDeleteView, BrandListView, BrandUpdateView
)

app_name = 'product'

urlpatterns = [
    # Product Paths
    path('', ProductListView.as_view(), name='list_products'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('<str:product_id>/', ProductDetailView.as_view(), name='get_by_id'),
    path('update_product/<str:product_id>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<str:product_id>/', ProductDeleteView.as_view(), name='delete_product'),
    path('discount/', ProductDiscountView.as_view(), name='apply_discount'),
    path('product_from_category_name/<str:title>/', ProductCategoryView.as_view(), name='product_from_category_name'),

    # Category Paths
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('update_category/<str:category_id>/', CategoryUpdateView.as_view(), name='update_category'),
    path('delete_category/<str:category_id>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('list_category/', CategoryListView.as_view(), name='list_category'),

    # Brand Paths
    path('create_brand/', BrandCreateView.as_view(), name='create_brand'),
    path('update_brand/<str:brand_id>/', BrandUpdateView.as_view(), name='update_brand'),
    path('delete_brand/<str:brand_id>/', BrandDeleteView.as_view(), name='delete_brand'),
    path('list_brand/', BrandListView.as_view(), name='list_brand'),
]
