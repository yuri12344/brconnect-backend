from .models import Product


class OrderService:
    """
    Service to handle orders.
    """
    def __init__(self, order):
        self.order = order
