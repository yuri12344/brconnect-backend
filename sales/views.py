from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderDataSerializer
from .services import HandleOrderFactory
import ipdb

class HandleOrder(APIView):
    """
    This class is to Handle the order from whatsapp, 
    who comes from one call via API and given token from company
    
    params:
        message_id: str
        client_name: str
        whatsapp_api_service: str
        whatsapp_api_session: str

    headers:
        Authorization: Token $Ppakd... (token from company)
    """
    permission_classes = [IsAuthenticated]

    # This endpoint is /api/v1/sales/handle_order
    def post(self, request):

        # Get serializer and validate data
        serializer = OrderDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        if not request.user.company:
            return Response({"message": "User has no company"}, status=400)

        # Get handler and handle order
        try:
            handler = HandleOrderFactory(request)
            handler.handle_order()
            return Response({"message": "data"})
        except Exception as e:
            return Response({"message": str(e)}, status=400)