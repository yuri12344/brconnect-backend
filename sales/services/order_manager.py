from products.models import Product, WhatsAppProductInfo
from core.services.services import ALERTS
from .types import ProductType
from django.utils import timezone
from sales.models import Order
from typing import List

import ipdb



class OrderManager:
    def __init__(self, request, customer):
        self.request    = request
        self.customer   = customer # I decided to include the customer here because I think will need more calls

    def create_customer_message(self, customer):
        messages = []
        message = f"Oii {customer.name} !  \n\n*Pedido recebido com sucesso, obrigado!* 🧀👍\n\n"
        if not customer.has_address():
            message += "Me envie o *endereço de entrega com*: \nRua, número, bairro, cidade e estado. 🧀 "
        else:
            message += f"*É esse mesmo o endereço?* \n\n{customer.street}, {customer.city} - {customer.state} \n\n*Confirma pra mim por favor*"
        return message
    

    def get_orders_client(self):
        return self.customer.orders.filter(paid=False, expires_at__gt=timezone.now())

    def create_client_order(self):
        ...

    def get_or_create_whatsapp_product_info_db(self, products: List[ProductType]):
        products_order = []
        for product in products:
            whatsapp_product_info = WhatsAppProductInfo.objects.filter(id=product.id, name='product_name').first()
            
            if whatsapp_product_info is None:
                base_product = Product.objects.filter(name=product.name).first()
                if base_product is None:
                    raise ValueError(f"Product base not found in database: {product.name}")
                
                whatsapp_product_info = WhatsAppProductInfo.objects.create(
                    id=product.id,
                    name=product.name + "ALERTA 102",
                    price=product.price,
                    quantity=product.quantity,
                    description=ALERTS["102"],
                    product=base_product
                )
            products_order.append(whatsapp_product_info)
        if not products_order:
            raise ValueError(f"No WhatsAppProductInfo found in database with given ids: {products}")
        return products_order
