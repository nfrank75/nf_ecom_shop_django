from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions  import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

import os
from decouple import config

import stripe
 
from .filters import OrderFilter

from .models import Order, OrderItem

from product.models import Product

from .serializers import OrderSerializer, OrderItemSerializer

from utils.helpers import get_current_host

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):

    filterset = OrderFilter(request.GET, queryset=Order.objects.all().order_by('id'))

    number_of_order = filterset.qs.count()

    # Pagination
    resPerPage = 1
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    

    # orders = Order.objects.all()  

    serializer = OrderSerializer(queryset, many=True)
 
    return Response({ 
        'number_of_order': number_of_order,
        'resPerPage':resPerPage,
        'orders': serializer.data 
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):

    order = get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order, many=False)
 
    return Response({ 'order': serializer.data })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):

    user = request.user
    
    data = request.data

    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({ 'error': 'No order items. At least one product on order!'}, status=status.HTTP_400_BAD_REQUEST)

    else:

        # create order

        total_amount = sum(item['price'] * item['quantity'] for item in order_items)

        order =  Order.objects.create(
            user = user,
            street = data['street'],
            city = data['city'],
            state = data['state'],
            zip_code = data['zip_code'],
            phone_no = data['phone_no'],
            country = data['country'],
            total_amount = total_amount
            )

        # Create order items and set order to order items
        for i in order_items:
            product = Product.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
                ) 

            # update product stock
            product.stock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response({ 'Order created successfully!': serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):

    order = get_object_or_404(Order, id=pk)

    order.status = request.data['status']
    order.save()

    serializer = OrderSerializer(order, many=False)
 
    return Response({ 'order': serializer.data })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_order(request, pk):

    order = get_object_or_404(Order, id=pk)

    if order:
        order.delete()
 
        return Response({ 'detail': 'Order deleted successfully!' })

    else:
 
        return Response({ 'detail': 'Order not found!' })
        

stripe.api_key = config('STRIPE_PRIVATE_KEY')     
# YOUR_DOMAIN = 'http://127.0.0.1:8000'
# YOUR_DOMAIN = get_current_host()
 