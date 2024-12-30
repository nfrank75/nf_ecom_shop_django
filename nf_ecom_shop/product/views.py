from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions  import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


from .serializers import ProductSerializer, ProductImagesSerializer, ReviewSerializer
from .models import Product, ProductImages, Review
from .filters import ProductsFilter



@api_view(['GET'])
def get_products(request):

    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))

    number_of_product = filterset.qs.count()

    # Pagination
    resPerPage = 5

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    
    serializer = ProductSerializer(queryset, many=True)

    return Response({
        'number_of_product': number_of_product,
        'resPerPage':resPerPage,
        'products': serializer.data
        })

@api_view(['GET'])
def get_product(request, pk):

    product = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializer(product, many=False)

    return Response({
        'product': serializer.data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def upload_product_images(request):

    data=request.data
    files = request.FILES.getlist('images')

    images= []
    for f in files:
        image = ProductImages.objects.create(product=Product(data['product']), image=f)
        images.append(image)

    serializer = ProductImagesSerializer(images, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def new_product(request):

    data = request.data
    
    serializer = ProductSerializer(data=data)

    if serializer.is_valid():

        product = Product.objects.create(**data, user=request.user)
        
        res = ProductSerializer(product, many=False)

        return Response({ 'product': res.data })

    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request, pk):

    data = request.data

    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({'error': 'You can not update this product'}, status=status.HTTP_403_FORBIDDEN)

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.category = data['category']
    product.brand = data['brand']
    product.ratings = data['ratings']
    product.stock = data['stock']

    product.save()

    serializer = ProductSerializer(product, many=False)

    return Response({ 'product': serializer.data })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({'error': 'You can not delete this product'}, status=status.HTTP_403_FORBIDDEN)


    args = {"product": pk}
    images = ProductImages.objects.filter(**args)
    for i in images:
        i.delete()

    product.delete()


    return Response({'details': 'Product is deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):

    user = request.user

    product = get_object_or_404(Product, id=pk)

    print('product', product)

    data = request.data

    print('data', data)

    review = product.reviews.filter(user=user)

    print('review', review)

    if int(data['rating']) <= 0 or int(data['rating']) > 5:
        
        return Response({ 'error': 'Please select rating between 1-5'}, status=status.HTTP_400_BAD_REQUEST) 

    elif review.exists():

        new_review = { 'rating': data['rating'], 'comment': data['comment'] }
        review.update(**new_review)

        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))

        product.ratings = rating['avg_ratings']
        product.save()

        return Response({ 'detail': 'Review updated successfully!' })

    else:
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))

        product.ratings = rating['avg_ratings']
        product.save()
        
        return Response({ 'detail': 'Review posted successfully!' })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):

    user = request.user

    product = get_object_or_404(Product, id=pk)

    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()

        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))

        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0

        product.ratings = rating['avg_ratings']
        product.save()
        
        return Response({ 'detail': 'Review deleted successfully!' })

    else:
        return Response({'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)


