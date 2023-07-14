from . import HandlerWPPConnectOrder, OrderManager
from .customer_managment import CustomerManager
from core.services.services import ALERTS
from .types import ProductType
from typing import List
import logging
import time
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
            raise ValueError(f"Customer not found and could not be created for this order, with name: {self.request.data['client_name']} and whatsapp: {self.request.data['client_phone']}")

        products_list_order: List[ProductType] = self.handler.get_order_by_message_id(message_id=self.request.data['message_id'])
        order_manager = OrderManager(self.request, customer, self.handler)
        
        # Messages creating
        order_received_msg = f"Oii {customer.name} !  \n\n*Pedido recebido com sucesso, obrigado!* 🧀👍\n\n"
        if not customer.has_address():
            order_received_msg += "Me envie o *endereço de entrega com*: \nRua, número, bairro, cidade e estado. 🧀 "
        else:
            order_received_msg += f"*É esse mesmo o endereço?* \n\n{customer.street}, {customer.city} - {customer.state} \n\n*Confirma pra mim por favor*"
        order_manager.create_customer_message(order_received_msg)

        if customer.has_order():
            order_manager.update_order(products_list_order)
            order_manager.create_customer_message("Seu pedido foi atualizado com sucesso! 🧀👍")

        elif not customer.has_order():
            order_manager.create_order(products_list_order)
            order_manager.create_customer_message("Seu pedido foi criado com sucesso! 🧀👍")

        # Send message queue
        # order_manager.send_messages(handler=self.handler, delay_s = 3)

        order_manager.get_recomendations()
        order_manager.send_recomendations()
        
