from simple_history.models import HistoricalRecords 
from products.models import Product, Coupon
from datetime import datetime, timedelta
from users.models import Customer, Company
from django.db import models

class Order(models.Model):
    """
    An Order represents a customer's order.
    """
    PAYMENT_METHODS_CHOICES = [
        ('D', 'Dinheiro'),
        ('C', 'Cartão'),
        ('B', 'Boleto'),
        ('P', 'Pix'),
    ]
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHODS_CHOICES, blank=False, null=False, default='P', verbose_name="Metodo de pagamento"
    )
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    coupon      = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Cupom")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Criado em: ")
    expires_at  = models.DateTimeField(default=lambda: datetime.now() + timedelta(days=7), verbose_name="Expira em: ")
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders', verbose_name="Empresa")

    class Meta:
        db_table = 'orders'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f'Pedido {self.id} para {self.customer.name}'

class ProductOrderItem(models.Model):
    """
    A ProductOrderItem represents a product in an order.
    """
    order       = models.ForeignKey(Order, related_name='product_order_items', on_delete=models.CASCADE, verbose_name="Pedido")
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantity    = models.PositiveIntegerField(verbose_name="Quantidade")

    class Meta:
        db_table = 'product_order_items'
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f'Item produto {self.id} do pedido {self.order.id}'


class Sale(models.Model):
    """
    A Sale represents a completed order.
    """
    STATUS_CHOICES = [
        (True, 'Pago'),
        (False, 'Não pago'),
    ]
    order   = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='sale', verbose_name="Pedido")
    paid    = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name="Pago")
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name="Pago em: ")
    history = HistoricalRecords(inherit=True)

    class Meta:
        db_table = 'sales'
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return f'Venda {self.id} para Pedido {self.order.id}'