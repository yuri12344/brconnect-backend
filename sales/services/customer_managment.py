from users.models import Customer
from ..serializers import OrderDataSerializer
import ipdb

class CustomerManager:
    def __init__(self, **kwargs):
        self.client_data = kwargs

    def get_or_create_client(self):
        customer, _ = Customer.objects.get_or_create(
            name        = self.client_data['name'],
            whatsapp    = self.client_data['whatsapp'],
            company     = self.client_data['company'],
            defaults    = {
                'name': self.client_data['name'],
                'whatsapp': self.client_data['whatsapp'],
                'company': self.client_data['company'],
            }
        )
        return customer