# admin.py
from .models import Company, Customer, CustomerGroup, Region, Interaction
from core.auxiliar import AdminBase
from django.contrib import admin

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'email', 'website')
    search_fields = ('name', 'city', 'state', 'email', 'website')

@admin.register(Customer)
class CustomerAdmin(AdminBase):
    list_display = ('name', 'whatsapp', 'phone', 'email', 'score')
    search_fields = ('name', 'whatsapp', 'phone', 'email')

@admin.register(CustomerGroup)
class CustomerGroupAdmin(AdminBase):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Region)
class RegionAdmin(AdminBase):
    list_display = ('regiao', 'cost')
    search_fields = ('regiao',)

@admin.register(Interaction)
class InteractionAdmin(AdminBase):
    list_display = ('name', 'description', 'date', 'score')
    search_fields = ('name', 'description')