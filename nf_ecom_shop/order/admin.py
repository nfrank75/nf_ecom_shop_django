from django.contrib import admin
from .models import Order, OrderItem

admin.site.site_header = "E-Commerce Rest API"
admin.site.site_title = "E-commerce Rest API"
admin.site.index_title = "E-commerce Rest API"

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'street',
        'city',
        'state',
        'zip_code',
        'phone_no',
        'country',
        'total_amount',
        'payment_status',
        'status',
        'payment_mode',
        'createdAt'
        )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'order',
        'name',
        'quantity',
        'price',
        'createdAt',
        )

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)