from rest_framework import serializers, exceptions
from .models import Order

class WhatsAppOrderDataSerializer(serializers.Serializer):
    message_id              = serializers.CharField(max_length=255, required=True)
    client_name             = serializers.CharField(max_length=50, required=True)
    client_phone            = serializers.CharField(max_length=20, required=True)
    whatsapp_session        = serializers.CharField(max_length=255, required=True)
    whatsapp_service        = serializers.CharField(max_length=50, required=True) 
    
    def validate(self, data):
        request = self.context.get('request')
        if request and not request.user.company:
            raise exceptions.ValidationError({"message": "User has no company"})
        return data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'