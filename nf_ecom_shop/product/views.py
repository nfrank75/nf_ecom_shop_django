from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions  import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


from .serializers import ProductSerializer, ProductImagesSerializer
from .models import Product, ProductImages
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
@permission_classes([IsAuthenticated])
def upload_product_images(request):

    data = request.data

    if product.user != request.user:
        return Response({'error': 'You can not upload the product images'}, status=status.HTTP_403_FORBIDDEN)


    files = request.FILES.getlist('images')

    images = []
    for f in files:
        image = ProductImages.objects.create(product=Product(data['product']), image=f)
        images.append(image)
    
    serializer = ProductImagesSerializer(images, many=True)

    print('serializer', serializer.data)
    print('data', data)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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