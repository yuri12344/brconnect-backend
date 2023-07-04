from whatsapp.models import WppConnectSession, TextMessage, ImageMessage, Campaign
from products.models import WhatsAppProductInfo
from users.models import Customer
from sales.models import Order
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
        return {"message_id": message_id, "base_products": base_products}
    
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

class WhatsAppOrderProcessingService:
    """
    Service to handle orders and product recommendations.
    """
    def __init__(self, company, message_id, client_phone, client_name):
        self.message_id         = message_id
        self.client_phone       = client_phone
        self.client_name        = client_name
        self.company            = company
        self.client             = self.get_client_instance()
        self.products           = None
        self.recommendations    = None
        self.whatsapp_client    = self.get_whatsapp_client()
        self.total_quantity     = None

    def get_client_instance(self):
        if not self.client_phone or not self.company:
            raise ValueError("Client phone and company must be set before getting client instance")

        client, created = Customer.objects.get_or_create(
            phone=self.client_phone,
            company=self.company,
            defaults={'name': self.client_name}
        )
        return client
    
    def fetch_products(self):
        self.products       = self.whatsapp_client.get_products_order_by_message_id(self.message_id)
        self.total_quantity = sum(product['quantity'] for product in self.products['base_products'])
        print(f"Products: {self.products}")
    
    def get_recommendations(self):
        if not self.products:
            self.fetch_products()

        if not self.products:
            raise Exception(f'Nenhum produto encontrado no message_id: {self.message_id}')
        
        
        # Verifica se o cliente já tem um pedido
        if self.client.has_order():
            print(f"O cliente {self.client.name} já tem um pedido. Não buscando recomendações.")
            return
        else:
            print(f"O cliente {self.client.name} não tem um pedido. Buscando recomendações.")
            self.create_order()

        categories_list = self._get_categories()

        if not categories_list:
            if self.total_quantity == 1:
                msg = "💳Para melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀"
                self.send_message(message=msg, phone=self.client_phone, is_group=None)
                return
            raise Exception('No categories found for products')
        products_for_recommendation = self._get_products_for_recommendation(categories_list)

        if not products_for_recommendation:
            if self.total_quantity == 1:
                message = "💳Para melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀"
                self.send_message(message=message, phone=self.client_phone, is_group=None)
                return
            raise Exception('No products found for recommendations')
        
        self._send_recommendation_messages(products_for_recommendation)

    def _get_categories(self):
        """Extracts all categories from the base products."""
        categories_list = set()
        for product in self.products['base_products']:
            categories = product.categories.all()
            for category in categories:
                categories_list.add(category)        
        return list(categories_list)

    def _get_products_for_recommendation(self, categories_list):
        """Finds products for recommendation based on category affinities."""
        products_for_recommendation = set()
        for category in categories_list:
            affinities = category.affinities_as_category1.all()
            for affinity in affinities:
                category2 = affinity.category2
                products = category2.products.all()
                for product in products:
                    product_categories = product.categories.all()
                    if not any(category in categories_list for category in product_categories) and product not in self.products['base_products']:
                        products_for_recommendation.add(product.whatsapp_info)
        return products_for_recommendation


    def _send_recommendation_messages(self, products_for_recommendation):
        """Sends recommendation messages for each product."""
        messages = self._create_recommendation_messages(products_for_recommendation)
        for message in messages:
            self.send_message(message=message, phone=self.client_phone, is_group=None)
            time.sleep(3)

    def _create_recommendation_messages(self, products_for_recommendation):
        """Creates recommendation messages for each product."""
        messages = []
        if self.total_quantity == 1:
            messages.append("💳Para melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀")
        
        messages.append("😊Abaixo algumas *sugestões* de produtos que *combinam* com a sua *compra:*")
        for product in products_for_recommendation:
            link = product.link if product.link else ""
            messages.append(f"*{product.product.name}:* {link}")
        messages.append("🧀 *Interessando*, é só *clicar* no link, *adicionar ao carrinho* e enviar que os carrinhos se somam.")
        return messages

    def create_order(self):
        if not self.products:
            raise Exception('No products fetched. Fetch products before getting recommendations.') 

        # Calcula o total do pedido
        total = sum(product.price for product in self.products['base_products'])

        # Cria o pedido
        order = Order.objects.create(
            company=self.company,
            customer=self.client,
            total=total,
            payment_method='P',  # Exemplo de método de pagamento
            paid=False,  # O pedido ainda não foi pago
        )

        return order

    def send_message(self, message, phone, is_group=None):
        self.whatsapp_client.send_text_message(message=message, phone=phone, is_group=is_group)

    def get_whatsapp_client(self):
        if self.company.whatsapp_service == 'wppconnect':
            return WppConnectService(self.company)
        elif self.company.whatsapp_service == 'baileys':
            return BaileysService(self.company)
        else:
            raise Exception('Invalid WhatsApp service')

