from django.contrib import admin
from .models import Product


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