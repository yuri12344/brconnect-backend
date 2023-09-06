from users.models import Customer
import ipdb

def get_or_create_customer(request) -> Customer:
    customer_data = {
        'name': request.data['client_name'],
        'whatsapp': request.data['client_phone'],
        'company': request.user.company,
    }
    customer, created = Customer.objects.get_or_create(**customer_data)
    if not created and not customer:
        info = f"Customer not found and could not be created with name: {customer_data['name']} and whatsapp: {customer_data['whatsapp']}"
        raise ValueError(info)
    return customer
