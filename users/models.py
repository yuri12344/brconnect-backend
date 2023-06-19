from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    description = models.TextField()

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sellers')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    unique_code = models.CharField(max_length=255, unique=True)
    whatsapp_number = models.CharField(max_length=15)
    pix = models.CharField(max_length=255)
    
    def calculate_commission(self):
        return sum(sale.commission for sale in self.sales.filter(paid=True))

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.user.username