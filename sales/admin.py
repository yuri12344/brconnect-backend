from django.contrib import admin
from .models import Sale, TicketOrderItem, ProductOrderItem

class TicketOrderInline(admin.TabularInline):
    model = TicketOrderItem
    extra = 1  
    readonly_fields = ['qr_code', 'used']

class ProductBaseClassAdmin(admin.ModelAdmin):
    inlines = [TicketOrderInline]

@admin.register(Sale)
class SaleAdmin(ProductBaseClassAdmin):
    readonly_fields = ['qr_code']

@admin.register(TicketOrderItem)
class TicketOrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ['used']

@admin.register(ProductOrderItem)
class ProductOrderItemAdmin(admin.ModelAdmin):
    pass

