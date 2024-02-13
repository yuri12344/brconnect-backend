from rest_framework import serializers, exceptions
from users.serializers import CustomerSerializer

from products.serializers import ProductSerializer

from .models import Order, ProductOrderItem

# Constantes para campos de escolha
WHATSAPP_SERVICE_CHOICES = ['wppconnect', 'codechat']

class WhatsAppOrderDataSerializer(serializers.Serializer):
    """
    Serializer para dados de pedidos do WhatsApp.
    """
    client_name = serializers.CharField(max_length=50, required=True)
    client_phone = serializers.CharField(max_length=20, required=True)
    whatsapp_session = serializers.CharField(max_length=255, required=True)
    whatsapp_service = serializers.ChoiceField(choices=WHATSAPP_SERVICE_CHOICES, required=True)
    order_json = serializers.JSONField(required=True)

    def validate(self, data):
        """
        Validação personalizada para garantir que o usuário pertence a uma empresa.
        """
        request = self.context.get('request')
        if request and not request.user.company:
            raise exceptions.ValidationError({"message": "User has no company"})
        return data


class ProductOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    class Meta:
        model = ProductOrderItem
        fields = [f.name for f in ProductOrderItem._meta.fields] + ['product']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Order.
    """
    customer = CustomerSerializer(read_only=True)  # Aninhe o CustomerSerializer aqui
    products = serializers.SerializerMethodField()
    
    def get_products(self, instance):
        product_order_items = instance.get_products()
        return ProductOrderItemSerializer(product_order_items, many=True).data

    class Meta:
        model = Order
        fields = [f.name for f in Order._meta.fields] + ['customer', 'products']  