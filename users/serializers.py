from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = [f.name for f in Customer._meta.fields] + ['address']  

    def get_address(self, instance):
        address = instance.get_address()
        if address:
            return address
        else:
            return "Endereço não disponível"