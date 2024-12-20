from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


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
def upload_product_images(request):

    data = request.data
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
def new_product(request):

    data = request.data

    serializer = ProductSerializer(data=data)

    if serializer.is_valid():

        product = Product.objects.create(**data)
        
        res = ProductSerializer(product, many=False)

        return Response({ 'product': serializer.data })

    else:
        return Response(serializer.errors)
    