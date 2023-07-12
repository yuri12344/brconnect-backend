from django.core.exceptions import ObjectDoesNotExist
from products.models import WhatsAppProductInfo, Product
from core.services.services import ALERTS
from .types import ProductType
from django.utils import timezone
from sales.models import Order, ProductOrderItem
from typing import List
import ipdb


class OrderManager:
    def __init__(self, request, customer):
        self.request    = request
        self.customer   = customer # I decided to include the customer here because I think will need more calls
        self.messages   = []

    def create_customer_message(self, message):
        self.messages.append(message)
        return self.messages
    

    def get_orders_client(self):
        return self.customer.orders.filter(paid=False, expires_at__gt=timezone.now())


    def create_order(self, products: List[ProductType]):
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

        return order


    
    def update_order(self, products: List[ProductType]):
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



