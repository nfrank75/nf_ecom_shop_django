from django.shortcuts import get_object_or_404, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from .serializers import ProductSerializer
from .models import Product
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
def get_product(request, pkk):

    product = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializer(product, many=False)

    return Response({
        'product': serializer.data
        })