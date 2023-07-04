from whatsapp.models import WppConnectSession, TextMessage, ImageMessage, Campaign
from products.models import WhatsAppProductInfo
from products.serializers import ProductSerializer
from abc import abstractmethod
import requests
import ipdb
import time

# services.py

class WhatsAppAPIService:
    @abstractmethod
    def fetch_products(self):
        pass

    @abstractmethod
    def send_text_message(self):
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
        self.session = self.get_wpp_connect_session()
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
        return {"message_id": message_id, "base_products": base_products}
    
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

    def get_wpp_connect_session(self):
        try:
            return WppConnectSession.objects.get(company=self.company)
        except WppConnectSession.DoesNotExist:
            raise Exception('WppConnectSession does not exist')

class WhatsAppOrderProcessingService:
    """
    Service to handle orders.
    """
    def __init__(self, company, message_id):
        self.company            = company
        self.message_id         = message_id
        self.whatsapp_client    = self.get_whatsapp_client()
        self.products           = None
        self.recomendations     = None

    def fetch_products(self):
        self.products = self.whatsapp_client.get_products_order_by_message_id(self.message_id)
    
    def get_recommendations(self):
        if not self.products:
            raise Exception('No products fetched. Fetch products before getting recommendations.')
        categories_list = []

        for product in self.products['base_products']:
            categories = product.categories.all()
            if len(categories) > 0:
                for categorie in categories:
                    categories_list.append(categorie)

        if len(categories_list) == 0:
            raise Exception('No categories found for products')

        time.sleep(3)
        products_for_recomendation = []
        for category in categories_list:
            affinities = category.affinities_as_category1.all()
            for affinity in affinities:
                category2 = affinity.category2
                products = category2.products.all()
                for product in products:
                    try:
                        products_for_recomendation.append(product.whatsapp_info)
                    except WhatsAppProductInfo.DoesNotExist:
                        raise Exception(f'{product} has no whatsapp info')

        messages = ["😊Abaixo algumas *sugestões* de produtos que *combinam* com a sua *compra:*"]

        for product in products_for_recomendation:
            link = product.link if product.link else ""
            messages.append(f"{product.product.name} - Link: {link}")

        messages.append("Caso tenha interesse em algum produto, é só me chamar! 😊")
        for message in messages:
            self.send_message(message=message, phone="554185115949")
            time.sleep(3)



    def send_message(self, message, phone, is_group=None):
        self.whatsapp_client.send_text_message(message=message, phone=phone, is_group=is_group)

    def get_whatsapp_client(self):
        if self.company.whatsapp_service == 'wppconnect':
            return WppConnectService(self.company)
        elif self.company.whatsapp_service == 'baileys':
            return BaileysService(self.company)
        else:
            raise Exception('Invalid WhatsApp service')
