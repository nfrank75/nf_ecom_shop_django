from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProductSerializer
from .models import Product


@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()
    
    serializer = ProductSerializer(products, many=True)

    return Response({
        'products': serializer.data
        })