from rest_framework import serializers

class OrderDataSerializer(serializers.Serializer):
    message_id = serializers.CharField(max_length=255, required=True)