import base64
import logging
import time

import ipdb
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from sales.models import Order
from users.models import Customer
from whatsapp.clients.whatsapp_client_service import WhatsAppClientService
from whatsapp.clients.whatsapp_interface import WhatsAppOrder

from .serializers import OrderSerializer, WhatsAppOrderDataSerializer
from .services.customer_managment import get_or_create_customer
from .services.types import SendMessage

logger = logging.getLogger("sales")


class OrderManager:
    def __init__(self, customer, whatsapp_order, company, whatsapp_client):
        self.customer = customer
        self.whatsapp_order = whatsapp_order
        self.company = company
        self.messages = []
        self.whatsapp_client = whatsapp_client
        self.use_case = []
        self.order = None

    def _send_messages(self):
        """Sends messages to the customer."""
        for message in self.messages:
            match message.type:
                case "SendMessage":
                    self.whatsapp_client.send_message(
                        phone=message.phone, message=message.message
                    )
                case "RecommendationMessage":
                    self.whatsapp_client.send_image_base64(
                        phone=message.phone,
                        caption=message.caption,
                        base64=message.base64,
                    )
            return {"message": "messages send sucessfully"}

    def create_or_update_order(self):
        if self.customer.has_order():
            """If customer has order, update it with new order"""
            order: Order = self.customer.orders.last()  # Take last order
            order.update_order_from_whatsapp_order(self.whatsapp_order)
        else:
            """Else, create it"""
            order = Order.create_order_from_whatsapp_order(
                self.whatsapp_order, self.customer, self.company
            )
        return order

    def define_which_use_case_is(self):
        customer_has_order = self.customer.has_order()
        quantity = self.whatsapp_order.total_quantity
        """ If client has no order and the whatsapp_order has only one product, send message to client """
        if not customer_has_order and quantity == 1:
            self.use_case.append(self._use_case_one_add_more_products_to_the_cart)

        """ If whatsapp_order > 1 quantity and dont have order in back-end, send recommendations """
        if not customer_has_order and quantity > 1:
            self.use_case.append(self._use_case_two_send_recommendations)

    def execute_use_case(self):
        if self.use_case:  # It can be cases that doenst not exists use cases
            for self.use_case in self.use_case:
                self.use_case()

    def _use_case_one_add_more_products_to_the_cart(self):
        self.messages.append(
            SendMessage(
                phone=self.customer.whatsapp,
                message="💳Para melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀",
            )
        )

    def _use_case_two_send_recommendations(self):
        recommendations = self.order.get_recommendations()
        if recommendations:
            for recommendation in recommendations:
                caption = recommendation.recommendation_text
                image_path = recommendation.recommendation_image.path
                time.sleep(5)
                # I tought is better send message here, because the load of image in base64
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode()
                    self.whatsapp_client.send_image_base64(
                        phone=self.customer.whatsapp,
                        filename="ok",
                        caption=caption,
                        base64=base64_image,
                    )
        else:
            return None

    def handle_order(self):
        self.define_which_use_case_is()
        self.order = self.create_or_update_order()

        self.execute_use_case()
        self._send_messages()


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

    # /api/v1/sales/handle_order
    def post(self, request):
        # Get serializer and validate data
        serializer = WhatsAppOrderDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        # Get handler and handle order
        try:
            customer: Customer = get_or_create_customer(request)
            whatsapp_client = WhatsAppClientService(request).get_client()
            company = request.user.company

            whatsapp_order: WhatsAppOrder = whatsapp_client.get_order_by_message_id(
                request.data["message_id"]
            )
            Product.create_products_in_back_end_from_whatsapp_order(
                whatsapp_order, company
            )
            order_manager = OrderManager(
                customer, whatsapp_order, company, whatsapp_client
            )
            order_manager.handle_order()

            return Response({"message": "data"})
        except Exception as e:
            logger.error(f"Error handling order: {str(e)}")
            return Response({"message": str(e)}, status=400)


class OrdersViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Order.objects.none()  # Return an empty queryset
        company = user.company
        return Order.objects.filter(company=company)
