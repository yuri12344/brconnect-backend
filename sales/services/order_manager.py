from products.models import Product
from core.services.services import ALERTS
from .types import ProductType
from .handlers import HandleWhatsAppOrderApi
from sales.models import Order, ProductOrderItem
from django.utils import timezone
from itertools import chain
from typing import List
from django.db import transaction
from django.db.models import F
import base64
import time
import ipdb

class OrderManager:
    def __init__(self, request, customer, handler: HandleWhatsAppOrderApi = None):
        self.request            = request
        self.customer           = customer # I decided to include the customer here because I think will need more calls
        self.order              = None
        self.recommendations    = []
        self.handler            = handler
        self.messages           = []
        self.categories         = []
        


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

        product_objects = []
        for product in products:
            try:
                product_instance = Product.objects.prefetch_related('categories').get(whatsapp_meta_id=product.id)
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

        with transaction.atomic():
            order.save()
            product_order_items = [
                ProductOrderItem(
                    order=order,
                    product=product['product'],
                    quantity=product['quantity'],
                    company=self.request.user.company,
                )
                for product in product_objects
            ]
            ProductOrderItem.objects.bulk_create(product_order_items)

            order.total = Order.calculate_total(order.product_order_items.all())
            order.save()

        self.order = order

    def update_order(self, products: List[ProductType]) -> None:
        if not products:
            raise ValueError("No products provided in update order.")

        self.order = self.customer.orders.last()

        if not self.order:
            raise ValueError("No existing order found for the customer in updating order.")

        new_products = []
        for product in products:
            try:
                product_instance = Product.objects.prefetch_related('categories').get(whatsapp_meta_id=product.id)
                new_products.append({
                    'product': product_instance,
                    'quantity': product.quantity
                })
            except Product.DoesNotExist:
                raise ValueError(f"Product not found with name: {product.name}")
        existing_items = {item.product.id: item for item in self.order.product_order_items.all()}

        with transaction.atomic():
            for product in new_products:
                if product['product'].id in existing_items:
                    # Update the quantity of the existing item
                    item = existing_items[product['product'].id]
                    item.quantity = item.quantity + product['quantity']  # Calculate new quantity in Python
                    item.save(update_fields=['quantity'])  # Ensure only the quantity field is updated
                else:
                    # Create a new ProductOrderItem
                    ProductOrderItem.objects.create(
                        order=self.order,
                        product=product['product'],
                        quantity=product['quantity'],  # Use the quantity from the ProductType
                        company=self.request.user.company,
                    )

            self.order.total = Order.calculate_total(self.order.product_order_items.all())
            self.order.save()



    def get_categories(self) -> set:
        self.categories = self.order.categories()
        return self.categories
    
    def get_recommendations(self):
        if not self.order:
            raise ValueError("No existing order found in get_recommendations.")

        all_recommendations = []
        for category in self.categories:
            all_recommendations.extend(category.recommendations_as_category_a.all())

        category_ids = {category.id for category in self.categories}
        recommendation_categories = set()  # Keep track of categories in recommendations

        for recommendation in all_recommendations:
            if recommendation.category_b.id not in category_ids and recommendation.category_b.id not in recommendation_categories:
                self.recommendations.append(recommendation)
                recommendation_categories.add(recommendation.category_b.id)  # Add category to the set

                
        return self.recommendations
    

    def send_recommendations(self):
        try:
            if not self.recommendations:
                raise ValueError("No existing recommendations found in send_recommendations.")
            
            for recomendation in self.recommendations:
                caption = recomendation.recommendation_text
                image_path = recomendation.recommendation_image.path
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
            print(f"Problema no send_recommendations: {e}")
            raise e