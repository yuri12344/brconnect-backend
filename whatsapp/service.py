from .models import WppConnectSession
from products.models import WhatsAppProductInfo
from abc import abstractmethod
import requests
import ipdb

# services.py

class WhatsAppAPIService:
    @abstractmethod
    def fetch_products(self):
        pass

    @abstractmethod
    def send_text_message(self):
        pass

    @abstractmethod
    def send_image_base64(self):
        pass

class BaileysService(WhatsAppAPIService):
    def fetch_products(self):
        ...
    
    def send_text_message(self):
        ...

class WppConnectService(WhatsAppAPIService):
    def __init__(self, company):
        self.company    = company
        self.session    = None
        self.base_url   = None
        self.token      = None
        self.headers    = None
        self.initial_setup()

    def initial_setup(self):
        self.session = self.get_client_wpp_session()
        self.token = self.session.session_token
        self.base_url = f'https://apiwpp.brconnect.click/api/{self.session.session_name}/'
        self.headers = {'accept': '*/*','Authorization': f'Bearer {self.token}'}
    
    # [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
    def get_products_order_by_message_id(self, message_id):
        """
        Retrieves order details by message ID from the WppConnect API.

        Args:
            message_id (str): The ID of the message for which to retrieve order details.

        Returns:
            list: A list of dictionaries, where each dictionary represents a product in the order.
                Each product dictionary includes only the 'id', 'price', 'name', and 'quantity' fields.
                If there are no products in the response, an empty list is returned.
        """
        url = f'{self.base_url}get-order-by-messageId'
        response = requests.get(
            url,
            headers=self.headers,
            json={'messageId': message_id}
        )
        response_data = response.json()
        raw_product_data = response_data.get('response', {}).get('data', [])

        # Extract only the 'id', 'price', 'name', and 'quantity' fields from each product.
        product_data = [
            {key: product[key] for key in ('id', 'price', 'name', 'quantity')}
            for product in raw_product_data
        ]
        # [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
        try:
            base_products = []
            for product in product_data:
                base_product = WhatsAppProductInfo.objects.get(id=product['id']).product
                base_products.append(base_product)
        except WhatsAppProductInfo.DoesNotExist:
            raise Exception(f'Product with ID {product["id"]} does not exist')
        return {"message_id": message_id, "base_products": base_products, "incoming_order": product_data}
    
    def send_image_base64(self, phone, is_group=None, base64=None, caption=None):
        ...

    def send_text_message(self, phone, is_group=None, message=""):
        """
        Sends a message using the WppConnect API.

        Args:
            phone (str): The phone number to which to send the message.
            is_group (bool): Whether the message is being sent to a group.
            message (str): The message to send.

        Returns:
            dict: The JSON response from the WppConnect API.
        """
        url = f'{self.base_url}send-message'
        data = {
            'phone': phone,
            'isGroup': is_group,
            'message': message
        }
        response = requests.post(
            url,
            headers=self.headers,
            json=data
        )
        return response.json()

    def get_client_wpp_session(self):
        try:
            return WppConnectSession.objects.get(company=self.company)
        except WppConnectSession.DoesNotExist:
            raise Exception('WppConnectSession does not exist')