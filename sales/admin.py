from .models import Order, ProductOrderItem, CollectionProduct, Coupon, Collection
from django.contrib import admin
from django.utils import timezone


class CollectionProductInline(admin.TabularInline):  # ou admin.StackedInline, dependendo de suas preferências
    model = CollectionProduct
    exclude = ('company',)  # Exclude the company field from the form
    extra = 1  # Número de linhas a serem exibidas.

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["collection", "product"]:
            if hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            else:
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        else:
            return qs.filter(company=request.user.company)
        
    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            if hasattr(request.user, 'employee'):
                obj.company = request.user.employee.company
            else:
                obj.company = request.user.company
        super().save_model(request, obj, form, change)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    exclude = ('company',)
    inlines = [CollectionProductInline]
    filter_horizontal = ('categories',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            if hasattr(request.user, 'employee'):
                obj.company = request.user.employee.company
            else:
                obj.company = request.user.company
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:  # Only set the company when the object is first created
                if hasattr(request.user, 'employee'):
                    instance.company = request.user.employee.company
                else:
                    instance.company = request.user.company
            instance.save()
        formset.save_m2m()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        else:
            return qs.filter(company=request.user.company)


class ProductOrderItemInline(admin.TabularInline):
    model = ProductOrderItem
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ('company',)  # Exclude the company field from the form
    inlines = [ProductOrderItemInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "customer" or db_field.name == "coupon":
            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            obj.company = request.user.company
        if obj.paid and obj.paid_at is None:
            obj.paid_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        else:
            return qs.filter(company=request.user.company)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    exclude = ('company',)  # Exclude the company field from the form
    filter_horizontal = ('categories', 'products', 'collections',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["category", "product", "collection"]:
            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ["categories", "products", "collections"]:
            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        else:
            return qs.filter(company=request.user.company)



