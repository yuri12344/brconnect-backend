from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderDataSerializer
from .services import HandleOrderFactory

from whatsapp.clients.whatsapp_client_service import WhatsAppClientService

import logging, ipdb
logger = logging.getLogger('sales')

class HandleOrder(APIView):
    """
    This class is to Handle the order from whatsapp, 
    who comes from API call and given company token     
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
        # Get handler and handle order
        try:
            ipdb.set_trace()
            whatsapp_client = WhatsAppClientService(request).get_client()
            handler = HandleOrderFactory(request)
            handler.handle_order()
            return Response({"message": "data"})
        except Exception as e:
            logger.error(f"Error handling order: {str(e)}")
            return Response({"message": str(e)}, status=400)