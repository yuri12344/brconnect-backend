from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProductOrder:
    price: float
    name: str
    quantity: int
    id: str = field(default='')
    thumbnailUrl: Optional[str] = field(default=None)
    currency: Optional[str] = field(default=None)
    
@dataclass
class WhatsAppOrder:
    products: list[ProductOrder] 
    total_quantity: int
    total_value: float  
    
class WhatsAppClientInterface:
    @abstractmethod
    def fetch_products(self):
        pass

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def send_image_base64(self):
        pass
    
    @abstractmethod
    def get_order_by_message_id(self) -> WhatsAppOrder:
        pass

    @abstractmethod
    def get_products_by_invoice_order_message_json(self) -> WhatsAppOrder:
        pass
