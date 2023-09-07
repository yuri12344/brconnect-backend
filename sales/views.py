from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderDataSerializer

from .services.customer_managment import get_or_create_customer
from users.models import Customer
from .services.order_workflow import OrderWorkflow


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
            customer: Customer      = get_or_create_customer(request)
            whatsapp_client         = WhatsAppClientService(request).get_client()
            order_flow = OrderWorkflow(
                company=request.user.company,
                customer=customer, 
                whatsapp_client=whatsapp_client,
                message_id = request.data['message_id']
            )
            order_flow._whatsapp_products_list()
            order_flow._create_products_in_back_end()
            order_flow._client_has_order_in_back_end()
            if order_flow.client_has_order_in_back_end:
                order_flow._get_last_order()
                order_flow._update_order()
            else:
                order_flow._create_order()
                
            order_flow._generate_messages()
            order_flow._send_messages()
                
            return Response({"message": "data"})
        except Exception as e:
            logger.error(f"Error handling order: {str(e)}")
            return Response({"message": str(e)}, status=400)