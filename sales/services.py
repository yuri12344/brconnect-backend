from .models import Product

class OrderService:
    """
    Service to handle orders.
    """
    def __init__(self, order):
        self.order = order

    def get_affinity_products(self):
        return Product.objects.filter(categories__in=self.order.categories.all())

    def get_recomendations(self):
        return Product.objects.filter(categories__in=self.order.categories.all())   
    
    def get_order_products(self):
        ...