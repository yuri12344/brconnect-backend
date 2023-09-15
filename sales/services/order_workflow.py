from .types import SendMessage, RecommendationMessage,  RecommendationMessage, SendMessage

import ipdb

class OrderWorkflow:
    def __init__(self, company, customer):
        self.company                                                = company
        self.customer                                               = customer
        self.messages: list[SendMessage | RecommendationMessage]    = []


    def _generate_messages(self):
        """
        Checks the quantities of products in the order and generates appropriate messages or recommendations.
        """
        if not self.whatsapp_order:
            self._whatsapp_order()
        if self.whatsapp_order.total_quantity == 1 and self._client_has_order_in_back_end():
            message = SendMessage(phone=self.customer.whatsapp, message="💳BACKENDPara melhorar o *custo benefício* de sua compra, sugerimos que *adicione mais um produto* por conta do *valor do frete.*🧀")
            self.messages.append(message)
        else:
            # ecommendations = self._get_recommendations()
            self.messages.append("Recomendation")