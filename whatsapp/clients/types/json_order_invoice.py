from dataclasses import dataclass, field
from typing import List

"""{
"reference_id":"4O5RA186IOB",
"type":"physical-goods",
"payment_configuration":"merchant_categorization_code",
"currency":"BRL",
"total_amount":{
    "value":207000,
    "offset":1000
},
"order_request_id":"400410239064805",
"order":{
    "status":"payment_requested",
    "items":[
        {
            "retailer_id":"5566191506783769",
            "name":"Requeijão de corte de Bufula Bubalat",
            "amount":{
            "value":69000,
            "offset":1000
            },
            "quantity":3,
            "isCustomItem":false,
            "isQuantitySet":true
        }
    ],
    "subtotal":{
        "value":207000,
        "offset":1000
    }
}
}"""

@dataclass
class Item:
    retailer_id: str
    product_id: str
    name: str
    amount: dict
    quantity: int
    isCustomItem: bool = False  # Default value provided
    isQuantitySet: bool = True  # Default value provided


@dataclass
class Order:
    status: str
    items: List[Item]
    subtotal: dict

@dataclass
class Transaction:
    reference_id: str
    type: str
    payment_configuration: str
    currency: str
    total_amount: dict
    order_request_id: str
    order: Order
