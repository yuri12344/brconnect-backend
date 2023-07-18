from users.models import Customer, BaseModel
from products.models import Product
from django.utils import timezone
from datetime import timedelta
from django.db import models
from typing import List

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

    def is_paid_and_not_expired(self):
        expiration_date = timezone.now() - timedelta(days=self.company.order_expiration_days)
        return not self.paid and self.date_created > expiration_date

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

