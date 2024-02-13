from .whatsapp_interface import WhatsAppClientInterface, WhatsAppOrder, ProductOrder
from ..models import WppConnectSession
from users.models import Company
import logging
import requests
import ipdb
import json
from dataclasses import asdict  # Import asdict to convert dataclass instances to dictionaries

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from whatsapp.clients.types.json_order_invoice import Item, Order, Transaction

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
            total_value=sum([(product.price / 1000) * product.quantity for product in formated_product_list]),
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
        
    def get_products_by_invoice_order_message_json(self, order_json: str) -> WhatsAppOrder:
        data = json.loads(order_json)
        
        # Convert each item in the order to a ProductOrder instance
        product_orders = []
        total_quantity = 0
        total_value = 0
        
        for item in data['order']['items']:
            # Assuming 'amount' contains the price per item and 'value' is in the smallest currency unit (e.g., centavos)
            price_per_item = item['amount']['value'] / 100.0  # Convert to standard currency unit
            quantity = item['quantity']
            
            product_order = ProductOrder(
                price=price_per_item,
                name=item['name'],
                quantity=quantity,
                id=item.get('product_id', ''),  # Assuming 'product_id' is the intended field for 'id'
                # Add more fields if available and necessary
            )
            
            product_orders.append(product_order)
            total_quantity += quantity
            total_value += price_per_item * quantity
        
        # Create the WhatsAppOrder instance
        whatsapp_order = WhatsAppOrder(
            products=product_orders,
            total_quantity=total_quantity,
            total_value=total_value
        )
        
        return whatsapp_order


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
