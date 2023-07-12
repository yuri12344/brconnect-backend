from django.core.exceptions import ObjectDoesNotExist
from products.models import WhatsAppProductInfo, Product
from core.services.services import ALERTS
from .types import ProductType
from django.utils import timezone
from sales.models import Order, ProductOrderItem
from typing import List
from .handlers import HandleWhatsAppOrderApi
import base64
from django.core.files.base import ContentFile
import time
import ipdb
from itertools import chain

class OrderManager:
    def __init__(self, request, customer, handler: HandleWhatsAppOrderApi = None):
        self.request        = request
        self.customer       = customer # I decided to include the customer here because I think will need more calls
        self.order          = None
        self.recomendations = None
        self.handler        = handler
        self.messages       = []

    def send_messages(self,  delay_s: int = 3) -> None:
        for message in self.messages:
            self.handler.whatsapp_client.send_message(message=message, phone=self.customer.whatsapp)
            time.sleep(delay_s)
        self.messages = []

    def send_image_base64(self, base64: str, delay_s: int = 3) -> None:
        self.handler.whatsapp_client.send_base64(base64=base64, phone=self.customer.whatsapp)
                                                 
    def create_customer_message(self, message) -> None:
        self.messages.append(message)

    def get_orders_client(self) -> List[Order]:
        return self.customer.orders.filter(paid=False, expires_at__gt=timezone.now())

    def create_order(self, products: List[ProductType]) -> None:
        if not products:
            raise ValueError("No products provided in create order.")

        # Map product IDs to quantities
        quantities = {product.id: product.quantity for product in products}

        # Get the corresponding Product or WhatsAppProductInfo objects
        product_objects = []
        for product in products:
            try:
                # Busca por ID no WhatsAppProductInfo
                product_objects.append(WhatsAppProductInfo.objects.get(id=product.id))
            except WhatsAppProductInfo.DoesNotExist:
                try:
                    # Busca por nome no WhatsAppProductInfo se a busca por ID falhar
                    product_objects.append(WhatsAppProductInfo.objects.get(name=product.name))
                except WhatsAppProductInfo.DoesNotExist:
                    try:
                        product_objects.append(Product.objects.get(name=product.name))
                    except Product.DoesNotExist:
                        raise ValueError(f"Product not found with name: {product.name}")

        order = Order(
            total=0,
            customer=self.customer,
            company=self.request.user.company,
            paid=False,
            expires_at=timezone.now() + timezone.timedelta(minutes=30),
        )
        order.save()

        for product in product_objects:
            if isinstance(product, WhatsAppProductInfo):
                ProductOrderItem.objects.create(
                    order=order,
                    product_whats=product,
                    quantity=quantities[product.id]  # Use the quantity from the ProductType
                )
            else:
                ProductOrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantities[product.id]  # Use the quantity from the ProductType
                )

        # Recalculate the total
        order.total = Order.calculate_total(order.product_order_items.all())
        order.save()
        self.order = order
    
    def update_order(self, products: List[ProductType]) -> None:
        if not products:
            raise ValueError("No products provided in update order.")

        # Get the last order of the customer
        self.order = self.customer.orders.last()

        if not self.order:
            raise ValueError("No existing order found for the customer in updating order.")

        # Map product IDs to quantities
        quantities = {product.id: product.quantity for product in products}

        # Get the corresponding Product or WhatsAppProductInfo objects
        product_objects = []
        for product in products:
            try:
                # Busca por ID no WhatsAppProductInfo
                product_objects.append(WhatsAppProductInfo.objects.get(id=product.id))
            except WhatsAppProductInfo.DoesNotExist:
                try:
                    # Busca por nome no WhatsAppProductInfo se a busca por ID falhar
                    product_objects.append(WhatsAppProductInfo.objects.get(name=product.name))
                except WhatsAppProductInfo.DoesNotExist:
                    try:
                        product_objects.append(Product.objects.get(name=product.name))
                    except Product.DoesNotExist:
                        raise ValueError(f"Product not found with name: {product.name}")


        for product in product_objects:
            if isinstance(product, WhatsAppProductInfo):
                item, created = ProductOrderItem.objects.get_or_create(
                    order=self.order,
                    product_whats=product,
                    defaults={'quantity': quantities[product.id]}  # Initial quantity if a new item is created
                )
                if not created:
                    item.quantity += quantities[product.id]  # Increase the quantity if the item already exists
                    item.save()
            else:
                item, created = ProductOrderItem.objects.get_or_create(
                    order=self.order,
                    product=product,
                    defaults={'quantity': quantities[product.id]}  # Initial quantity if a new item is created
                )
                if not created:
                    item.quantity += quantities[product.id]  # Increase the quantity if the item already exists
                    item.save()

        # Recalculate the total
        self.order.total = Order.calculate_total(self.order.product_order_items.all())
        self.order.save()

    def get_recomendations(self):
        if not self.order:
            raise ValueError("No existing order found in get_recomendations.")
        
        order_categories = list(chain.from_iterable(item.product_whats.product.categories.all() for item in self.order.product_order_items.all()))
        order_categorie_affinity = []
        for category in order_categories: 
            order_categorie_affinity = list(chain.from_iterable(category.affinities_as_category1.all() for category in order_categories))
        

        recomendations = {}
        for category_afinity in order_categorie_affinity:
            if not category_afinity.category2 in order_categories:
                featured_products           = list((category_afinity.category2.featured_products.all()))
                whats_app_products_links    = [product.whatsapp_info.link for product in featured_products if product.whatsapp_info]
                
                image_path = category_afinity.image.path
                with open(image_path, 'rb') as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode()

                    recomendation_data = {
                        'image_base64': base64_image,
                        'whats_app_products_links': whats_app_products_links
                    }
                    recomendations.append(recomendation_data)
                
        self.recomendations = recomendations

    def send_recomendations(self):
        if not self.recomendations:
            raise ValueError("No existing recomendations found in send_recomendations.")
        msg = "Ola obrigado por comprar, segue as recomendações: \n\n"
        for recomendation in self.recomendations:
            for link in recomendation['whats_app_products_links']:
                msg += link
        phone = self.customer.whatsapp 
        filename ="ok"
        caption = msg
        base64 = recomendation['image_base64']

        self.handler.whatsapp_client.send_image_base64(
            phone=phone,
            filename=filename,
            caption=caption,
            base64=base64
        )