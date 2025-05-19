# product_management/urls.py

from django.urls import path
from .views import  get_all_products, create_product, get_product, add_product, update_product, delete_product

urlpatterns = [
    path('products/', get_all_products, name='get_all_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<uuid:product_id>/get/', get_product, name='get_product'),
    path('products/add/', add_product, name='add_product'),
    path('products/<uuid:product_id>/update/', update_product, name='update_product'),
    path('products/<uuid:product_id>/delete/', delete_product, name='delete_product'),
]
