from dataclasses import dataclass
from products.models import Product

# [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
@dataclass
class WhatsAppProduct:
    id: str
    price: int
    name: str
    quantity: int
    
@dataclass
class SendMessage:
    type = "SendMessage"
    phone: str
    message: str

@dataclass
class RecommendationMessage:
    type = "RecommendationMessage"
    phone: str
    caption: str
    base64: str
    
@dataclass
class ProductQuantityOrder:
    product: Product
    quantity: int
    
@dataclass
class WhatsAppOrder:
    total_quantity: int
    products: list[ProductQuantityOrder]