from django.urls import path
from .views import register, current_user, update_user

urlpatterns = [
    path('register/', register, name="register"),
    path('me/', current_user, name="current_user"),
    path('me/update', update_user, name="update_user"),
]