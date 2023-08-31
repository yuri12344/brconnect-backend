from .codechat import CodeChatWhatsAppClient
from .wppconnect import WppConnectWhatsAppClient
from .whatsapp_interface import WhatsAppClientInterface

from typing import Type

class WhatsAppClientService:
    def __init__(self, request):
        self.request = request
        self.client = self.get_client()
        
    def get_client(self) -> Type[WhatsAppClientInterface]:
        """
        Retorna uma instância do cliente de WhatsApp com base no serviço especificado.
        
        :raises ValueError: Se o serviço de API especificado é inválido.
        """
        whatsapp_service = self.request.data.get('whatsapp_service')
        
        whatsapp_session    = self.request.data["whatsapp_session"]
        company             = self.request.user.company
        
        match whatsapp_service:
            case 'wppconnect':
                return WppConnectWhatsAppClient(whatsapp_session=whatsapp_session, company=company)
            case 'codechat':
                return CodeChatWhatsAppClient(whatsapp_session=whatsapp_session, company=company)
            case _:
                raise ValueError(f"Invalid API service. Valid options are: 'codechat', 'wppconnect'")

        
