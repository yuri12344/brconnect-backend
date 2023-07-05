from django.core.exceptions import ValidationError
from .models import Customer, Company, Interaction
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib import admin


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ('owner',)  # Exclude the owner field from the form
    readonly_fields = ('owner_token',)

    def owner_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj.owner)
        return token.key

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(id=request.user.employee.company.id)
        else:
            return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the owner when the object is first created
            if Company.objects.filter(owner=request.user).exists():
                messages.error(request, "Você já possui uma empresa.")
                return
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ('company',)  # Exclude the company field from the form
    filter_horizontal = ('preferences', 'purchase_history',)
    search_fields = ('name', 'phone',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        elif hasattr(request.user, 'company'):
            return qs.filter(company=request.user.company)
        else:
            messages.warning(request, "Você precisa criar uma empresa antes de ver clientes.")
            return qs.none()

    def save_model(self, request, obj, form, change):
        try:
            if not change:  # Only set the company when the object is first created
                obj.company = request.user.company
            super().save_model(request, obj, form, change)
        except AttributeError:
            raise ValidationError("Você precisa criar uma empresa antes de adicionar clientes.")


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    exclude = ('company',)  # Exclude the company field from the form
    filter_horizontal = ('customers', )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "customers":
            if request.user.is_superuser:
                kwargs["queryset"] = Customer.objects.all()
            elif hasattr(request.user, 'employee'):
                kwargs["queryset"] = Customer.objects.filter(company=request.user.employee.company)
            elif hasattr(request.user, 'company'):
                kwargs["queryset"] = Customer.objects.filter(company=request.user.company)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        elif hasattr(request.user, 'company'):
            return qs.filter(company=request.user.company)
        else:
            messages.warning(request, "Você precisa criar uma empresa antes de criar interações.")
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            obj.company = request.user.company
        super().save_model(request, obj, form, change)
