from .whatsapp_interface import WhatsAppClientInterface, WhatsAppOrder, ProductOrder
from ..models import WppConnectSession
from users.models import Company
import logging
import requests
import ipdb




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WppConnectWhatsAppClient(WhatsAppClientInterface):
    def __init__(
            self, 
            company: Company, 
            whatsapp_session = None
        ):
        self.company = company
        self.session = WppConnectSession.objects.get(
            company=company,
            whatsapp_api_session=whatsapp_session
        )
        
    def _format_order(self, raw_product_list: list[dict]) -> WhatsAppOrder:
        if not raw_product_list:
            raise ValueError("Raw product list cannot be empty")
        formated_product_list = []
        for product in raw_product_list:
            formated_product_list.append(ProductOrder(
                id=product['id'],
                name=product['name'],
                price=product['price'],
                quantity=product['quantity']
            ))
        return WhatsAppOrder(
            total_quantity=sum([product.quantity for product in formated_product_list]),
            total_value=sum([product.price * product.quantity for product in formated_product_list]),
            products=formated_product_list
        )
        
    # [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
    def _get_order_by_message_id(self, message_id: str):
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

    def get_order_by_message_id(self, message_id: str) -> WhatsAppOrder:
        raw_product_list = self._get_order_by_message_id(message_id)
        return self._format_order(raw_product_list)
        
        
    def send_image_base64(self, phone: str, is_group: bool = False, filename="", caption="", base64: str = None):
        if not phone or not base64:
            raise ValueError("Phone or base64 string cannot be empty")
        if not base64.startswith('data:image/png;base64,'):
            base64 = 'data:image/png;base64,' + base64
        data = {
            'phone': str(phone),
            'isGroup': is_group,
            'filename': str(filename),
            'caption': str(caption),
            'base64': base64 + str(base64)
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
            logger.error(f"Request send image base64 failed: {e}, response: {response.json()}")
            return None

        response_data = response.json()
        return response_data
    

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
