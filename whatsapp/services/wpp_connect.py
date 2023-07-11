from ..models import WppConnectSession
from users.models import Company
from . import WhatsAppAPIService
import logging
import requests

import ipdb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)



class WppConnectService(WhatsAppAPIService):
    whatsapp_api_service = 'wppconnect'
    def __init__(self, company: Company, whatsapp_api_session = None):
        self.company = company
        self.session = WppConnectSession.objects.get(
            company=company,
            whatsapp_api_session=whatsapp_api_session
        )

    # [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
    def get_order_by_message_id(self, message_id: str):
        if not message_id:
            raise ValueError("Message id cannot be empty")
        
        url = self.session.url + '/get-order-by-messageId'
        try:
            response = requests.get(
                url,
                headers=self.session.headers,
                json={'messageId': message_id}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # handle error
            logger.error(f"Request get_order_from_api wppConnect failed: {e}")
            return None

        response_data = response.json()
        return response_data.get('response', {}).get('data', [])

        
    def send_image_base64(self, phone: str, is_group: bool = False, filename="", caption="", base64: str = None):
        if not phone or not base64:
            raise ValueError("Phone or base64 string cannot be empty")

        data = {
            'phone': str(phone),
            'isGroup': is_group,
            'filename': str(filename),
            'caption': str(caption),
            'base64': str(base64)
        }
        url = self.session.url + '/send-image'

        try:
            response = requests.post(
                url,
                headers=self.session.headers,
                json=data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request send image base64 failed: {e}")
            return None

        response_data = response.json()
        return response_data.get('response', {}).get('data', [])
    

    def send_message(self, phone, is_group=None, message=""):
        if not phone or not message:
            raise ValueError("Phone or message cannot be empty")

        data = {
            'phone': str(phone),
            'isGroup': is_group,
            'message': str(message)
        }
        url = self.session.url + '/send-message'
        try:
            response = requests.post(
                url,
                headers=self.session.headers,
                json=data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # handle error
            print(f"Request send message failed: {e}")
            return None
        return {"message": "Message sent successfully"}
