from django.urls import path
from .views import get_products, get_product, upload_product_images

urlpatterns = [
    path('products/', get_products, name="products"),
    path('products/upload_images/', upload_product_images, name="upload_images"),
    path('products/<str:pk>/', get_product, name="get_product_details"),
]