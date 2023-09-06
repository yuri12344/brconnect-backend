from users.models import Customer, BaseModel
from products.models import Product
from django.utils import timezone
from datetime import timedelta
from django.db import models
from typing import List
import ipdb

class Order(BaseModel):
    """
    An Order represents a customer's order.
    """
    PAYMENT_METHODS_CHOICES = [
        ('D', 'Dinheiro'),
        ('C', 'Cartão'),
        ('B', 'Boleto'),
        ('P', 'Pix'),
    ]
    STATUS_CHOICES = [
        (True, 'Pago'),
        (False, 'Não pago'),
    ]
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHODS_CHOICES, blank=False, null=False, default='P', verbose_name="Metodo de pagamento"
    )
    paid        = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name="Pago")
    paid_at     = models.DateTimeField(auto_now_add=True, verbose_name="Pago em: ")
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")

    class Meta:
        db_table = 'orders'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def categories(self):
        categories_set = set()
        product_order_items = self.product_order_items.prefetch_related('product__categories').all()
        for product in product_order_items:
            product_categories = product.product.categories.all()
            categories_set = categories_set.union(product_categories)
        return categories_set

    def is_paid_and_not_expired(self):
        
        ...
        
    def is_paid(self):
        """
        Verifica se a ordem está paga e não expirada.
        
        Uma ordem é considerada não expirada se a data de criação da ordem é posterior à data de expiração calculada.
        
        Retorna:
            bool: True se a ordem está paga e não expirada, caso contrário False.
        """
        return True if self.paid else False
    
    def is_expired(self):
        company_expiration_date_days = self.company.order_expiration_days
        return True if self.date_created < timezone.now() - timedelta(days=company_expiration_date_days) else False
        

    @staticmethod
    def calculate_total(product_order_items: List['ProductOrderItem']):
        total = 0
        for item in product_order_items:
            total += item.product.price * item.quantity
        return total

    def __str__(self):
        return f'Pedido para {self.customer.name}'

class ProductOrderItem(BaseModel):
    """
    A ProductOrderItem represents a product in an order.
    """
    order           = models.ForeignKey(Order, related_name='product_order_items', on_delete=models.CASCADE, verbose_name="Pedido")
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto", null=True, blank=True)
    quantity        = models.PositiveIntegerField(verbose_name="Quantidade", default=1)

    class Meta:
        db_table = 'product_order_items'
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f'Item produto {self.id} do pedido {self.order.id}'

