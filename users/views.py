from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Check if the request is authenticated
        if self.request.user.is_authenticated:
            # Limit the queryset to the customers of the company that provided the token
            return Customer.objects.filter(company=self.request.user.company)
        else:
            # Return an empty queryset
            return Customer.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if the request is authenticated
            if self.request.user.is_authenticated:
                # Set the company of the created customer to the company that provided the token
                serializer.save(company=self.request.user.company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)