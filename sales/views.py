from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderView(APIView):
    def get(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"message": "Successful login!"})
        else:
            return Response({"error": "Wrong username or password"}, status=status.HTTP_400_BAD_REQUEST)