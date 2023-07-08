from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderDataSerializer
from .services import HandleOrderFactory
import ipdb

class HandleOrder(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = OrderDataSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.company:
                return Response({"message": "User has no company"}, status=400)
            try:
                data = request.data
                handler = HandleOrderFactory(request).get_handler()
                order = handler.whatsapp_client.get_order_by_message_id(message_id=data['message_id'])
                ipdb.set_trace()
                return Response({"message": "data"})
            except Exception as e:
                return Response({"message": str(e)}, status=400)
        
        else:
            return Response(serializer.errors, status=400)