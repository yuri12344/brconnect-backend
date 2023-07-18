from . import HandlerWPPConnectOrder, OrderManager
from .customer_managment import CustomerManager
from .types import ProductType
from typing import List
import ipdb


class HandleOrderFactory:
    HANDLERS = {
        'wppconnect': HandlerWPPConnectOrder,
        # 'baileys': HandlerBaileysOrder,
    }

    def __init__(self, request):
        self.request = request
        self.whatsapp_api_service = self.request.data.get('whatsapp_api_service')
        self.whatsapp_api_session = self.request.data.get('whatsapp_api_session')
        self.handler = self.get_handler()

    def get_handler(self):
        handler_class = self.HANDLERS.get(self.whatsapp_api_service)
        if handler_class is None:
            raise ValueError("Invalid provider")
        return handler_class(company=self.request.user.company, whatsapp_api_session=self.whatsapp_api_session)
    

    def handle_order(self):
        customer_info = {
            'name': self.request.data['client_name'],
            'whatsapp': self.request.data['client_phone'],
            'company': self.request.user.company,
        }
        customer_manager = CustomerManager(**customer_info)
        customer = customer_manager.get_or_create_client()

        if not customer:
            info = f"Customer not found and could not be created for this order \
                     with name: {self.request.data['client_name']} and whatsapp: {self.request.data['client_phone']}"
            raise ValueError(info)

        products_list_order: List[ProductType] = self.handler.get_order_by_message_id(message_id=self.request.data['message_id'])
        order_manager = OrderManager(self.request, customer, self.handler)
        
        if customer.has_order():
            order_manager.update_order(products_list_order)
            return {'status': 'order updated'}
        else:
            order_manager.create_order(products_list_order)
            order_manager.get_categories()
            order_manager.get_recomendations()
            if order_manager.recomendations:
                order_manager.send_recomendations()
        

