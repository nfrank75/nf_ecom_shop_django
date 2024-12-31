from django.urls import path
from .views import (new_order, get_orders, get_order,
                    process_order, delete_order, 
                    create_checkout_session, stripe_webhook
                    )

urlpatterns = [
    path('', get_orders, name="get_orders"),
    path('new_order/', new_order, name="new_order"),
    path('<str:pk>/get_order/', get_order, name="get_order"),
    path('<str:pk>/process_order/', process_order, name="process_order"),
    path('<str:pk>/delete/', delete_order, name="delete_order"),

    path('create-checkout-session/', create_checkout_session, name="create_checkout_session"),
    
    path('webhook/', stripe_webhook, name="stripe_webhook"),
]