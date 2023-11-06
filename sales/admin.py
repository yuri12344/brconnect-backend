from .models import Order, ProductOrderItem
from core.auxiliar import CompanyAdminMixin, AdminBase
from django.contrib import admin
class ProductOrderItemTabularInline(CompanyAdminMixin, admin.StackedInline):
    model = ProductOrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(AdminBase):
    list_display = ('customer', 'total', 'amount_paid', 'amount_missing', 'paid_at', 'date_created')
    search_fields = ('customer__name', 'customer__email', 'customer__cpf')
    list_filter = ('amount_paid', 'date_created')
    inlines = [ProductOrderItemTabularInline]