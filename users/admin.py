from django.core.exceptions import ValidationError
from .models import Customer, Company, Interaction
from django.contrib import messages
from django.contrib import admin


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ('owner',)  # Exclude the owner field from the form

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
    filter_horizontal = ('preferences', )
    
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


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            obj.company = request.user.company
        super().save_model(request, obj, form, change)