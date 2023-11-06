from abc import abstractmethod
from collections import defaultdict

from users.models import Customer, BaseModel
from products.models import Product
from django.utils import timezone
from datetime import timedelta
from django.db import models
import ipdb
from whatsapp.clients.whatsapp_interface import WhatsAppOrder

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
        ('Cancelado', 'Cancelado'),
        ('Não enviado', 'Não enviado'),
        ('Separado', 'Separado'),
        ('Enviado', 'Enviado'),
        ('Recebido', 'Recebido'),
    ]
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHODS_CHOICES, blank=False, null=False, default='P', verbose_name="Metodo de pagamento"
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor pago")
    amount_missing = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Falta pagar")
    status      = models.CharField(choices=STATUS_CHOICES, default='Não enviado', verbose_name="Status", null=True, blank=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Chama o método save original para salvar o objeto Order
        self.total = self.calculate_total()  # Atualiza o total com a quantidade de produtos
        self.amount_missing = self.get_total_missing()  # Atualiza o total com a quantidade de produtos
        super().save(update_fields=['total', 'amount_missing'])  # Salva o objeto Order novamente com o total atualizado

    def get_total_missing(self):
        return self.total - self.amount_paid

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
            recommendation_categories = set()  # Keep track of categories in recommendations

            for recommendation in all_recommendations:
                if recommendation.category_b.id not in category_ids and recommendation.category_b.id not in recommendation_categories:
                    recommendations.append(recommendation)
                    recommendation_categories.add(recommendation.category_b.id)  # Add category to the set
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
            product_instance_in_whatsapp_cart = Product.objects.get(whatsapp_meta_id=product.id)
            product_order_item = self.product_order_items.filter(product=product_instance_in_whatsapp_cart).first()
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
            ProductOrderItem.objects.create(
                company=company,
                order=order,
                product=Product.objects.get(whatsapp_meta_id=product.id),
                quantity=product.quantity,
            )
        return order
        
    def is_paid(self):
        return True if self.paid else False
    
    def is_expired(self):
        company_expiration_date_days = self.company.order_expiration_days
        return True if self.date_created < timezone.now() - timedelta(days=company_expiration_date_days) else False

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

