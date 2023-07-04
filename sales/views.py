from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderDataSerializer
from .services import WhatsAppOrderProcessingService
import ipdb

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = OrderDataSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.company:
                return Response({"message": "User has no company"}, status=400)
            try:
                whatsapp_order_service = WhatsAppOrderProcessingService(
                    company = request.user.company,
                    message_id = serializer.data["message_id"],
                    client_name = serializer.data["client_name"],
                    client_phone = serializer.data["client_phone"],
                )
                ipdb.set_trace()
                whatsapp_order_service.fetch_products()
                whatsapp_order_service.get_recommendations()

                return Response({"message": "data"})
            except Exception as e:
                return Response({"message": str(e)}, status=400)
        
        else:
            return Response(serializer.errors, status=400)