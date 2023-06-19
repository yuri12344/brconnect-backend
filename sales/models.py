from datetime import datetime, timedelta

from django.db import models

from core.auxiliar import QRCodeMixin
from products.models import Product, Ticket
from users.models import Customer, Seller

    
class Sale(QRCodeMixin, models.Model):
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(choices=STATUS_CHOICES, default=False)
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHODS_CHOICES, blank=False, null=False, default='P'
    )
    expires_at = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, related_name='sales')
    commission = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def get_qr_data(self):
        return {'User': self.user.username, 'Order': self.pk}
    
    class Meta:
        db_table = 'sales'

    def __str__(self):
        if self.seller:
            return f'Sale {self.id} by {self.seller.user.username} to {self.customer.user.username}'
        else:
            return f'Sale {self.id} by company to {self.customer.user.username}'

    

class ProductOrderItem(QRCodeMixin, models.Model):
    buy_order = models.ForeignKey(Sale, related_name='product_order_item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    used = models.BooleanField(default=False)
    
    def get_qr_data(self):
        return {'User': self.buy_order.user.user.username, 'Order': self.pk}
    
    class Meta:
        db_table = 'product_order_item'

    def __str__(self):
        return f'Item produto {self.id} da ordem de compra {self.buy_order.id}'


class TicketOrderItem(QRCodeMixin, models.Model):
    buy_order = models.ForeignKey(Sale, related_name='ticket_order_item', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    used = models.BooleanField(default=False)

    def get_qr_data(self):
        return {'User': self.buy_order.user.user.username, 'Order': self.pk}

    
    class Meta:
        db_table = 'ticket_order_item'

    def __str__(self):
        return f'Item ticket {self.id} da ordem de compra {self.buy_order.id}'

