from .types import RecommendationMessage, SendMessage

from sales.models import Order
from .types import WhatsAppProduct, ProductQuantityOrder, WhatsAppOrder, SendMessage, RecommendationMessage
from sales.models import Order, ProductOrderItem
from django.db import transaction
from products.models import Product

import ipdb

class OrderWorkflow:
    def __init__(self, company, customer, whatsapp_client, message_id):
        self.company                                                = company
        self.customer                                               = customer
        self.whatsapp_client                                        = whatsapp_client
        self.message_id                                             = message_id
        self.whatsapp_products                                      = []
        self.whatsapp_order:WhatsAppOrder                           = None
        self.messages: list[SendMessage | RecommendationMessage]    = []
        self.client_has_order_in_back_end:bool                      = False
        self.product_objects: list[ProductQuantityOrder]            = []
    
    def _client_has_order_in_back_end(self) -> bool:
        self.client_has_order_in_back_end = self.customer.has_order()
        return self.client_has_order_in_back_end
    
    def _create_products_in_back_end(self) -> None:
        """Create products in backend"""
        if not self.whatsapp_products:
            self._whatsapp_products_list()
        for product in self.whatsapp_products:
            Product.objects.get_or_create(
                whatsapp_meta_id=product.id,
                defaults={
                    'name': product.name,
                    'price': product.price,
                    'company': self.company,
                    'description': 'INSERIR DESCRIÇÃO'
                }
            )
            
        
    def _get_recommendations(self) -> list[RecommendationMessage]:
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

    def _whatsapp_order(self):
        if not self.whatsapp_products:
            self._whatsapp_products_list()
        self.whatsapp_order = WhatsAppOrder(
            total_quantity=sum([product.quantity for product in self.whatsapp_products]),
            products=self.whatsapp_products
        )
        return self.whatsapp_order
 
    def _whatsapp_products_list(self) -> list[WhatsAppProduct]:
        if not self.message_id:
            raise Exception("Message id is required")
        
        whatsapp_raw_product_list = self.whatsapp_client.get_order_by_message_id(message_id=self.message_id)
        formated_product_list = []
        for product in whatsapp_raw_product_list:
            formated_product_list.append(WhatsAppProduct(
                id=product['id'],
                name=product['name'],
                price=product['price'],
                quantity=product['quantity']
            ))
        self.whatsapp_products = formated_product_list
        return self.whatsapp_products
            
    def _get_last_order(self) -> Order:
        self.order = self.customer.orders.last()
        return self.order

    def _update_order(self) -> None:
        if not self.whatsapp_products:
            self._whatsapp_products_list()
        existing_items = {item.product.whatsapp_meta_id: item for item in self.order.product_order_items.all()}
        if not existing_items:
            raise Exception("Problem in update, order has no items")
        
        with transaction.atomic():
            for product in self.whatsapp_products:
                if product.id in existing_items:
                    # Update the quantity of the existing item in order
                    item = existing_items[product.id]
                    item.quantity = item.quantity + product.quantity 
                    item.save(update_fields=['quantity']) 
                else:
                    ipdb.set_trace()
                    # Create a new ProductOrderItem with new products
                    ProductOrderItem.objects.create(
                        order=self.order,
                        product=product,
                        quantity=product.quantity,  # Use the quantity from the WhatsAppProduct
                        company=self.company,
                    )
            self.order.total = Order.calculate_total(self.order.product_order_items.all())
            self.order.save()
            
    def _create_product_order_items(self):
        with transaction.atomic():
            product_order_items = [
                ProductOrderItem(
                    order=self.order,
                    product=product_quantity_order.product,
                    quantity=product_quantity_order.quantity,
                    company=self.company,
                )
                for product_quantity_order in self.product_objects
            ]
            ProductOrderItem.objects.bulk_create(product_order_items)
            self.order.total = Order.calculate_total(self.order.product_order_items.all())
            self.order.save()
        return self.order
        
    def _get_products_and_quantities(self) -> list[ProductQuantityOrder]:
        product_objects = []
        for product in self.whatsapp_products:
            product_instance = Product.objects.get(
                whatsapp_meta_id=product.id,
            )
            product_objects.append(ProductQuantityOrder(
                product=product_instance,
                quantity=product.quantity
            ))
        self.product_objects = product_objects
        return self.product_objects
             
    def _create_order(self) -> Order:
        self._get_products_and_quantities()
        self.order = Order(
            total=0,
            customer=self.customer,
            company=self.company,
            paid=False,
        )
        # Put the product items inside of the order
        self.order.save()
        self._create_product_order_items()
        return self.order

    def _generate_messages(self):
        """
        Checks the quantities of products in the order and generates appropriate messages or recommendations.
        """
        if not self.whatsapp_order:
            self._whatsapp_order()
        if self.whatsapp_order.total_quantity == 1 and self._client_has_order_in_back_end():
            message = SendMessage(phone=self.customer.whatsapp, message="💳BACKENDPara melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀")
            self.messages.append(message)
        else:
            # ecommendations = self._get_recommendations()
            self.messages.append("Recomendation")

    def _send_messages(self):
        """
        Sends messages to the customer.
        """
        # Logic for sending messages
        for message in self.messages:
            match message.type:
                case "SendMessage":
                    self.whatsapp_client.send_message(
                        phone=message.phone, 
                        message=message.message
                    )
                case "RecommendationMessage":
                    self.whatsapp_client.send_image_base64(
                        phone=message.phone, 
                        caption=message.caption, 
                        base64=message.base64
                    )
        return {"message": "messages send sucessfully"}
