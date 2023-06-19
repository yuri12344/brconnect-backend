from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords
from users.models import Company

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)
    history = HistoricalRecords(inherit=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductBaseClass(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Supondo que você tem um modelo Categoria
    commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    history = HistoricalRecords(inherit=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    
    class Meta:
        db_table = 'product_base_class'

    def __str__(self):
        return self.name


class Ticket(ProductBaseClass):
    half_entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'tickets'


class Product(ProductBaseClass):
    stock = models.IntegerField()
    class Meta:
        db_table = 'products'


class ProductImage(models.Model):
    product = models.ForeignKey(ProductBaseClass, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'images'

    def __str__(self):
        return self.url