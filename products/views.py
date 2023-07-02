from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import viewsets

from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class useCasesByProductViewSet(viewsets.ViewSet):
    def list(self, request):
        body = request.data
        products = Product.objects.all()
        return Response({"products": f"products useCases o body é {body}"})
    

