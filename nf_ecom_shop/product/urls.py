from django.urls import path
from .views import (
    get_products, get_product, upload_product_images, new_product, 
    update_product, delete_product, create_review, delete_review)

urlpatterns = [
    path('', get_products, name="products"),
    path('new_product/', new_product, name="new_product"),
    path('upload_images/', upload_product_images, name="upload_product_images"),
    path('<str:pk>/', get_product, name="get_product_details"),
    path('<str:pk>/delete/', delete_product, name="delete_product"),
    path('<str:pk>/update/', update_product, name="update_product"),
    path('<str:pk>/review/', create_review, name="create_review"),
    path('<str:pk>/review/delete', delete_review, name="delete_review"),
]