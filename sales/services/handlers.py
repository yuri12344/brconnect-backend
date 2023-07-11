from whatsapp.services.wpp_connect import WppConnectService
from abc import ABC, abstractmethod
from .types import ProductType
from typing import List


class HandleWhatsAppOrderApi(ABC):
    def get_whatsapp_client(self, company, ServiceClass, whatsapp_api_session):
        try:
            return ServiceClass(company=company, whatsapp_api_session=whatsapp_api_session)
        except Exception as e:
            raise ValueError(f"Error getting WhatsApp client: {e}")

    @abstractmethod
    def get_order_by_message_id(self, message_id: str) -> List[ProductType]:
        pass


class HandlerWPPConnectOrder(HandleWhatsAppOrderApi):
    name = 'WppConnect'
    def __init__(self, company, whatsapp_api_session):
        self.session_name = whatsapp_api_session
        self.whatsapp_client = self.get_whatsapp_client(company, WppConnectService, whatsapp_api_session)
    
    def get_order_by_message_id(self, message_id) -> List[ProductType]:
        result = []
        products = self.whatsapp_client.get_order_by_message_id(message_id=message_id)
        if products:
            for product in products:
                result.append(ProductType(
                    id=product['id'],
                    price=product['price'],
                    name=product['name'],
                    quantity=product['quantity']
                ))
        if not result:
            raise ValueError("No products found")
        return result
    
