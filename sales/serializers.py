from rest_framework import serializers, exceptions
from users.models import Customer
from .models import Order

# Constantes para campos de escolha
WHATSAPP_SERVICE_CHOICES = ['wppconnect', 'codechat']

class WhatsAppOrderDataSerializer(serializers.Serializer):
    """
    Serializer para dados de pedidos do WhatsApp.
    """
    message_id = serializers.CharField(max_length=255, required=True)
    client_name = serializers.CharField(max_length=50, required=True)
    client_phone = serializers.CharField(max_length=20, required=True)
    whatsapp_session = serializers.CharField(max_length=255, required=True)
    whatsapp_service = serializers.ChoiceField(choices=WHATSAPP_SERVICE_CHOICES, required=True)

    def validate(self, data):
        """
        Validação personalizada para garantir que o usuário pertence a uma empresa.
        """
        request = self.context.get('request')
        if request and not request.user.company:
            raise exceptions.ValidationError({"message": "User has no company"})
        return data

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Customer.
    """
    address = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ('name', 'address',)
        
    def get_address(self, instance):
        address = instance.get_address()
        if address:
            return address
        else:
            return "Endereço não disponível"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Order.
    """
    customer = CustomerSerializer(read_only=True)  # Aninhe o CustomerSerializer aqui

    class Meta:
        model = Order
        fields = [f.name for f in Order._meta.fields] + ['customer']  # Inclua 'customer' aqui