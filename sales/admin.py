from core.mixins.mixins import CompanyAdminMixin, ExportCsvMixin
from .models import Order, ProductOrderItem
from django.contrib import admin
from core.auxiliar import AdminBase
from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import ProductOrderItem, Product 
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList

class ProductOrderItemForm(forms.ModelForm):
    class Meta:
        model = ProductOrderItem
        fields = '__all__'
        widgets = {
            'product': ForeignKeyRawIdWidget(ProductOrderItem._meta.get_field('product').remote_field, admin.site),
        }
        
class ProductOrderItemTabularInline(CompanyAdminMixin, admin.TabularInline):
    model = ProductOrderItem
    form = ProductOrderItemForm
    extra = 0
    readonly_fields = ('product_price', 'total_item_value')

    def product_price(self, obj):
        return obj.product.price if obj.product else 0
    product_price.short_description = 'Preço do Produto'

    def total_item_value(self, obj):
        return obj.total
    total_item_value.short_description = 'Total'

    fields = ('product', 'quantity', 'product_price', 'total_item_value')




class NotPaidFilter(admin.SimpleListFilter):
    title = _('não pagos')
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ('No', _('Não')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No':
            return queryset.filter(amount_paid__lt=F('total'))

class NotSentFilter(admin.SimpleListFilter):
    title = _('não enviados')
    parameter_name = 'sent'

    def lookups(self, request, model_admin):
        return (
            ('No', _('Não')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No':
            return queryset.filter(status='Não Enviado')  # Ajuste o critério conforme seu modelo

class TotalChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super().get_results(*args, **kwargs)
        self.total_amount = self.queryset.aggregate(Sum('total'))['total__sum']
        self.total_paid = self.queryset.aggregate(Sum('amount_paid'))['amount_paid__sum']
        

@admin.register(Order)
class OrderAdmin(AdminBase):
    change_form_template = 'admin/sales/change_form.html'
    list_display = (
        "customer",
        "total",
        "amount_paid",
        "paid_at",
        "date_created",
    )
    search_fields = ("customer__name", "customer__email")
    list_filter = ("amount_paid", "date_created", NotPaidFilter, NotSentFilter)
    inlines = [ProductOrderItemTabularInline]
    readonly_fields = ("amount_missing_display", "customer_phone", "customer_address")

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'customer',
                    'customer_phone',
                    'customer_address',
                    'total',
                    'amount_paid',
                    'amount_missing_display',
                    'status',
                    'payment_method'
                )
            }),
        ]
        return fieldsets

    def amount_missing_display(self, obj):
        return obj.get_total_missing()
    amount_missing_display.short_description = 'Valor Faltante'

    def customer_phone(self, obj):
        return obj.customer.whatsapp
    customer_phone.short_description = 'WhatsApp'

    def customer_address(self, obj):
        return obj.customer.get_address()
    customer_address.short_description = 'Endereço do Cliente'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ProductOrderItem) and not instance.company_id:
                instance.company = request.user.company
            instance.save()
        formset.save_m2m()
        
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            my_cl = response.context_data['cl']
            response.context_data['summary'] = {
                'total_amount': my_cl.total_amount,
                'total_paid': my_cl.total_paid,
                'total_missing': my_cl.total_missing,
            }
        except (AttributeError, KeyError):
            pass
        return response
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
