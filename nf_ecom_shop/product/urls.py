from django.urls import path
from .views import get_products, get_product, upload_product_images, new_product, update_product, delete_product

urlpatterns = [
    path('products/', get_products, name="products"),
    path('products/new_product/', new_product, name="new_product"),
    path('products/upload_images/', upload_product_images, name="upload_product_images"),
    path('products/<str:pk>/', get_product, name="get_product_details"),
    path('products/<str:pk>/delete/', delete_product, name="delete_product"),
    path('products/<str:pk>/update/', update_product, name="update_product"),
]