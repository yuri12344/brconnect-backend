from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer


class LoginView(APIView):
    def post(self, request, format=None):
        """
        Authenticate a user and return a token.
        """
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adiciona esta linha

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)
