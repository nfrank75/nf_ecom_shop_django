from rest_framework import serializers
from .models import Product, ProductImages, Review



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

    
class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImagesSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'user', 'reviews','images')

        extra_kwargs = {
            "name": { "required": True, },
            "description": { "required": True,},
            "price": { "required": True,},
            "brand": { "required": True,},
            "category": { "required": True, "allow_blank": False},
            "stock": { "required": True,},
            }

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    
        
        

