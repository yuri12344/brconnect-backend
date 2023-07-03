from .models import Product

class OrderService:
    """
    Service to handle orders.
    """
    def __init__(self, order):
        self.order = order

    def get_affinity_products(self):
        """
        Get products from affinity categories.
        """
        products = Product.objects.filter(categories__in=self.order.categories.all())
        return products

    def get_recomendations(self):
        """
        Get products from affinity categories.
        """
        products = Product.objects.filter(categories__in=self.order.categories.all())
        return products