from abc import abstractmethod
from collections import defaultdict
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

import ipdb
from django.db import models
from django.utils import timezone

from products.models import Product
from users.models import BaseModel, Customer
from whatsapp.clients.whatsapp_interface import WhatsAppOrder


class Order(BaseModel):
    PAYMENT_METHODS_CHOICES = [
        ("D", "Dinheiro"),
        ("C", "Cartão"),
        ("B", "Boleto"),
        ("P", "Pix"),
    ]

    STATUS_CHOICES = [
        ("Cancelado", "Cancelado"),
        ("Não enviado", "Não enviado"),
        ("Separado", "Separado"),
        ("Enviado", "Enviado"),
        ("Recebido", "Recebido"),
    ]
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Total"
    )
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Valor pago"
    )
    payment_method = models.CharField(
        max_length=255,
        choices=PAYMENT_METHODS_CHOICES,
        blank=False,
        null=False,
        default="P",
        verbose_name="Metodo de pagamento",
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default="Não enviado",
        verbose_name="Status",
        null=True,
        blank=True,
        max_length=100,
    )
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name="Pago em: ")
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Cliente",
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def categories(self):
        categories_set = set()
        product_order_items = self.product_order_items.prefetch_related(
            "product__categories"
        ).all()
        for product in product_order_items:
            product_categories = product.product.categories.all()
            categories_set = categories_set.union(product_categories)
        return categories_set

    def get_total_missing(self):
        return self.total - self.amount_paid
    
    def save(self, *args, **kwargs):
        # Se o objeto já tem um ID, é uma atualização.
        if self.id:
            self.total = self.calculate_total()
            super(Order, self).save(*args, **kwargs)
        else:
            # Se não tem um ID, é um novo objeto. Salve para obter um ID.
            super(Order, self).save(*args, **kwargs)

        
    def get_total_products_quantity(self):
        x = 0
        for product in self.product_order_items.all():
            x += product.quantity
        return x

    def get_recommendations(self):
        """
        The main problem I'm trying to solve here, is, if they have recommendations, we should give then the text message and
        the base64 file, btw, we should not do that, if the 2° categorie, is already in the order. Because its like
        we are recommending wine, for who already bought wine
        """
        categories = list(self.categories())

        recommendations = []
        all_recommendations = []
        if categories:
            for category in categories:
                all_recommendations.extend(category.recommendations_as_category_a.all())

            category_ids = {category.id for category in categories}
            recommendation_categories = (
                set()
            )  # Keep track of categories in recommendations

            for recommendation in all_recommendations:
                if (
                    recommendation.category_b.id not in category_ids
                    and recommendation.category_b.id not in recommendation_categories
                ):
                    recommendations.append(recommendation)
                    recommendation_categories.add(
                        recommendation.category_b.id
                    ) 
            return recommendations
        else:
            return None

    def calculate_total(self):
        total = 0
        for product in self.product_order_items.all():
            total += product.product.price * product.quantity
        return total

    def update_order_from_whatsapp_order(self, whatsapp_order: WhatsAppOrder):
        # add quantity for same products, and create new products
        for product in whatsapp_order.products:
            product_instance_in_whatsapp_cart = Product.objects.get(
                whatsapp_meta_id=product.id
            )
            product_order_item = self.product_order_items.filter(
                product=product_instance_in_whatsapp_cart
            ).first()
            if product_order_item:
                product_order_item.quantity += product.quantity
                product_order_item.save()
            else:
                ProductOrderItem.objects.create(
                    company=self.company,
                    order=self,
                    product=product_instance_in_whatsapp_cart,
                    quantity=product.quantity,
                )
        self.total = self.calculate_total()
        self.save()
        return self

    def get_products(self):
        return self.product_order_items.all()

    @abstractmethod
    def create_order_from_whatsapp_order(whatsapp_order: WhatsAppOrder, customer, company):
        order = Order.objects.create(
            company=company,
            customer=customer,
            total=whatsapp_order.total_value,
            payment_method="D",
        )
        for product in whatsapp_order.products:
            product_obj, created = Product.objects.get_or_create(
                whatsapp_meta_id=product.id, 
                company=company,
                price=product.price,
            )
            ProductOrderItem.objects.create(
                company=company,
                order=order,
                product=product_obj,
                quantity=product.quantity,
            )
        return order

    def is_paid(self):
        return self.amount_paid == self.total

    def is_expired(self):
        company_expiration_date_days = self.company.order_expiration_days
        return (
            True
            if self.date_created
            < timezone.now() - timedelta(days=company_expiration_date_days)
            else False
        )

    def __str__(self):
        return f"Pedido para {self.customer.name}"

class OrderToSupplier(BaseModel):
    class RequestStatus(models.TextChoices):
        NOT_REQUESTED = "NR", "Não solicitado"
        REQUESTED = "RQ", "Solicitado"
        DELIVERED = "DL", "Entregue"

    orders = models.ManyToManyField(
        "Order", related_name="orders_to_supplier", verbose_name="Pedidos"
    )
    supplier = models.ForeignKey(
        "users.Supplier",
        on_delete=models.CASCADE,
        related_name="supplier_orders",
        verbose_name="Fornecedor",
    )
    request_status = models.CharField(
        max_length=2,
        choices=RequestStatus.choices,
        default=RequestStatus.NOT_REQUESTED,
        verbose_name="Status da Solicitação",
    )
    # Outros campos que você possa precisar

    def __str__(self):
        return f"Pedido para {self.supplier.name} - Status: {self.get_request_status_display()}"


class ProductOrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        related_name="product_order_items",
        on_delete=models.CASCADE,
        verbose_name="Pedido",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Produto", null=True, blank=True
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=1, verbose_name="Quantidade"
    )
 
    status = models.CharField(
        max_length=20,
        choices=[
            ("not_requested", "Não solicitado"),
            ("requested", "Solicitado"),
            ("delivered", "Entregue"),
        ],
        default="not_requested",
        verbose_name="Status da Solicitação",
    )
    def calculate_total(self):
        return "{:.2f}".format(self.quantity * self.product.price) if self.product else "0.00"

    @property
    def total(self):
        return self.calculate_total()


    class Meta:
        db_table = "product_order_items"
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.product.name} x {self.quantity} no Pedido {self.order.id}"

