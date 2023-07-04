from rest_framework import serializers

class OrderDataSerializer(serializers.Serializer):
    message_id      = serializers.CharField(max_length=255, required=True)
    client_name     = serializers.CharField(max_length=50, required=True)
    client_phone   = serializers.CharField(max_length=20, required=True)