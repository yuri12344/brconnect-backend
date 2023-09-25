from rest_framework import viewsets
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer

from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer  
    
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Product.objects.none()  # Return an empty queryset
        company = user.company
        return Product.objects.filter(empresa=company)
