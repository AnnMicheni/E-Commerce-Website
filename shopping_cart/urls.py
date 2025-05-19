from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart),
    path('update/', views.update_cart_item),
    path('remove/', views.remove_from_cart),
]
