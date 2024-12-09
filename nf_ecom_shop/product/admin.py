from django.contrib import admin
from .models import Product

admin.site.site_header = "E-Commerce Rest API"
admin.site.site_title = "E-commerce Rest API"
admin.site.index_title = "E-commerce Rest API"

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'price',
        'brand',
        'category',
        'ratings',
        'stock',
        'user',
        'is_active',
        )


admin.site.register(Product, ProductAdmin)