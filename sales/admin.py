from django.contrib import admin

from core.auxiliar import AdminBase
from core.mixins.mixins import CompanyAdminMixin, ExportCsvMixin

from .models import Order, ProductOrderItem


class ProductOrderItemTabularInline(CompanyAdminMixin, admin.StackedInline):
    model = ProductOrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(AdminBase):
    list_display = (
        "customer",
        "total",
        "amount_paid",
        "amount_missing",
        "paid_at",
        "date_created",
    )
    search_fields = ("customer__name", "customer__email")
    list_filter = ("amount_paid", "date_created")
    inlines = [ProductOrderItemTabularInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ProductOrderItem) and not instance.company_id:
                instance.company = request.user.company
            instance.save()
        formset.save_m2m()


@admin.register(ProductOrderItem)
class ProductOrderItemAdmin(ExportCsvMixin, AdminBase):
    list_display = (
        "order",
        "product",
        "quantity",
    )
    search_fields = (
        "order__customer__name",
        "order__customer__email",
        "order__customer__cpf",
        "product__name",
    )
    list_filter = ("status", "order__date_created")
