from django.urls import path
from .views import get_products, get_product

urlpatterns = [
    path('products/', get_products, name="products"),
    path('products/<str:pk>/', get_product, name="get_product_details")
]