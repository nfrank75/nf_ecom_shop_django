from django.contrib import admin
from .models import Product, ProductImages, Review

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

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'rating',
        'comment',
        'user',
        )


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductImages)