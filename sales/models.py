from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords 
from products.models import Product, Category, WhatsAppProductInfo
from datetime import datetime, timedelta
from users.models import Customer, Company
from django.db import models
from django.utils import timezone


def get_expiration_date():
    return datetime.now() + timedelta(days=7)


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
    coupon      = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Cupom")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Criado em: ")
    expires_at  = models.DateTimeField(default=get_expiration_date, verbose_name="Expira em: ")
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders', verbose_name="Empresa")
    history     = HistoricalRecords(inherit=True)

    class Meta:
        db_table = 'orders'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def is_paid_and_not_expired(self):
            return not self.paid and timezone.now() < self.expires_at

    def __str__(self):
        return f'Pedido {self.pk} para {self.customer.name}'


class ProductOrderItem(models.Model):
    """
    A ProductOrderItem represents a product in an order.
    """
    order           = models.ForeignKey(Order, related_name='product_order_items', on_delete=models.CASCADE, verbose_name="Pedido")
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto", null=True, blank=True)
    product_whats   = models.ForeignKey(WhatsAppProductInfo, on_delete=models.CASCADE, verbose_name="Produto WhatsApp", null=True, blank=True)
    quantity        = models.PositiveIntegerField(verbose_name="Quantidade", default=1)

    class Meta:
        db_table = 'product_order_items'
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f'Item produto {self.id} do pedido {self.order.id}'


class Collection(models.Model):
    """
    A Collection represents a showcase of products.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    categories = models.ManyToManyField(Category, related_name='collections', verbose_name="Categorias", blank=True)
    products = models.ManyToManyField(Product, through='CollectionProduct', related_name='collections', related_query_name='collection', blank=True, verbose_name="Produtos")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Empresa")

    class Meta:
        db_table = 'collections'
        verbose_name = "Coleção"
        verbose_name_plural = "Coleções"

    def __str__(self):
        return self.name
    

class CollectionProduct(models.Model):
    """
    A CollectionProduct represents the relationship between a Collection and a Product.
    """
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name="Collection")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Data adicionado")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='collection_products', verbose_name="Empresa")

    class Meta:
        db_table = 'collection_products'
        verbose_name = "Produto da Collection"
        verbose_name_plural = "Produtos da Collection"

    def __str__(self) -> str:
        return self.collection.name + ' - ' + self.product.name
    

class Coupon(models.Model):
    """
    A Coupon represents a discount code that can be applied to products or categories.
    """
    code = models.CharField(max_length=255, unique=True, verbose_name="Codigo")
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, help_text="Desconto em %", verbose_name="Desconto")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    categories = models.ManyToManyField(Category, related_name='coupons', related_query_name='coupon', blank=True, verbose_name="Categoria")
    products = models.ManyToManyField(Product, related_name='coupons', related_query_name='coupon', blank=True, verbose_name="Produto")
    collections = models.ManyToManyField(Collection, related_name='coupons', related_query_name='coupon', blank=True, verbose_name="Coleção")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='coupons', verbose_name="Empresa")
    expires_at  = models.DateTimeField(default=get_expiration_date, verbose_name="Expira em: ")

    class Meta:
        db_table = 'coupons'
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"

    def __str__(self):
        return self.code