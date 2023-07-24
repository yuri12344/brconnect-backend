from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request, format=None):
        """
        Authenticate a user and return a token.
        """
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
