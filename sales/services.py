from abc import ABC, abstractmethod
from whatsapp.services import WppConnectService
from dataclasses import dataclass
from typing import List
import ipdb
# [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    

@dataclass
class ProductType:
    id: str
    price: int
    name: str
    quantity: int


class HandleOrder(ABC):
    def get_whatsapp_client(self, company, ServiceClass, whatsapp_api_session):
        try:
            return ServiceClass(company=company, whatsapp_api_session=whatsapp_api_session)
        except Exception as e:
            raise ValueError(f"Error getting WhatsApp client: {e}")

    @abstractmethod
    def get_order_by_message_id(self, message_id: str) -> List[ProductType]:
        pass

class HandlerWPPConnectOrder(HandleOrder):
    name = 'WppConnect'
    def __init__(self, company, whatsapp_api_session):
        self.session_name = whatsapp_api_session
        self.whatsapp_client = self.get_whatsapp_client(company, WppConnectService, whatsapp_api_session)
    
    def get_order_by_message_id(self, message_id) -> List[ProductType]:
        return self.whatsapp_client.get_order_by_message_id(message_id=message_id)

class HandleOrderFactory:
    def __init__(self, request):
        self.whatsapp_api_service = request.data['whatsapp_api_service']
        self.whatsapp_api_session = request.data['whatsapp_api_session']
        self.company = request.user.company

    def get_handler(self):
        if self.whatsapp_api_service == 'wppconnect':
            return HandlerWPPConnectOrder(company=self.company, whatsapp_api_session=self.whatsapp_api_session )
        elif self.whatsapp_api_service == 'baileys':
            return "Implement Baileys"
        else:
            raise ValueError("Invalid provider")

        