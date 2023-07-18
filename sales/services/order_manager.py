from products.models import Product
from core.services.services import ALERTS
from .types import ProductType
from .handlers import HandleWhatsAppOrderApi
from sales.models import Order, ProductOrderItem
from django.utils import timezone
from itertools import chain
from typing import List
import base64
import time
import ipdb

class OrderManager:
    def __init__(self, request, customer, handler: HandleWhatsAppOrderApi = None):
        self.request        = request
        self.customer       = customer # I decided to include the customer here because I think will need more calls
        self.order          = None
        self.recomendations = []
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

        # Get the corresponding Product or WhatsAppProductInfo objects
        product_objects = []
        for product in products:
            try:
                product_instance = Product.objects.get(whatsapp_meta_id=product.id)
                product_objects.append({
                    'product': product_instance,
                    'quantity': product.quantity
                })
            except Product.DoesNotExist:
                raise ValueError(f"Product not found with name: {product.name}")
        order = Order(
            total=0,
            customer=self.customer,
            company=self.request.user.company,
            paid=False,
        )
        
        order.save()
        for product in product_objects:
            ProductOrderItem.objects.create(
                order=order,
                product=product['product'],
                quantity=product['quantity'],  # Use the quantity from the ProductType
                company=self.request.user.company,
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

        new_products = []
        for product in products:
            try:
                product_instance = Product.objects.get(whatsapp_meta_id=product.id)
                new_products.append({
                    'product': product_instance,
                    'quantity': product.quantity
                })
            except Product.DoesNotExist:
                raise ValueError(f"Product not found with name: {product.name}")

        existing_items = {item.product.id: item for item in self.order.product_order_items.all()}
        for product in new_products:
            # Check if the product is already in the order
            if product['product'].id in existing_items:
                # Update the quantity of the existing item
                item = existing_items[product['product'].id]
                item.quantity += product['quantity']
                item.save()
            else:
                # Create a new ProductOrderItem
                ProductOrderItem.objects.create(
                    order=self.order,
                    product=product['product'],
                    quantity=product['quantity']
                )

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

        for category_afinity in order_categorie_affinity:
            if not category_afinity.category2 in order_categories:
                featured_products           = list((category_afinity.category2.featured_products.all()))
                whats_app_products_links    = [product.whatsapp_info.link for product in featured_products if product.whatsapp_info]
 
                recomendation_data = {
                    'text_recomendation': category_afinity.text_recomendation,
                    'image_path': category_afinity.image.path,
                    'whats_app_products_links': whats_app_products_links[0]
                }
                self.recomendations.append(recomendation_data)

    def send_recomendations(self):
        try:
            if not self.recomendations:
                raise ValueError("No existing recomendations found in send_recomendations.")
            for recomendation in self.recomendations:
                caption = recomendation['text_recomendation'] + '\n\n'
                caption += recomendation['whats_app_products_links'] if recomendation['whats_app_products_links'] else ""
                image_path = recomendation['image_path']

                time.sleep(5)
                with open(image_path, 'rb') as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode()
                    self.handler.whatsapp_client.send_image_base64(
                        phone=self.customer.whatsapp,
                        filename="ok",
                        caption=caption,
                        base64=base64_image
                    )
        except Exception as e:
            print(f"Problema no send_recomendations: {e}")
            raise e