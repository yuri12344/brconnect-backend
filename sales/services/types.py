from dataclasses import dataclass

# [{'id': '4317646281673903', 'price': 56000, 'name': 'Provolone maturado por 2 meses', 'quantity': 1}]    
@dataclass
class ProductType:
    id: str
    price: int
    name: str
    quantity: int