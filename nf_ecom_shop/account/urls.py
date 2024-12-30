from django.urls import path
from .views import register, current_user, update_user, forgot_password, reset_password

urlpatterns = [
    path('register/', register, name="register"),
    path('me/', current_user, name="current_user"),
    path('me/update', update_user, name="update_user"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('reset_password/<str:token>', reset_password, name="reset_password "),
]