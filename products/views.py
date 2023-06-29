from rest_framework.response import Response
from rest_framework.views import APIView

class ProductsView(APIView):
    def get(self, request):
        data = {'key': 'value'}
        return Response(data)

