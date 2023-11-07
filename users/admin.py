# admin.py
from .models import Company, Customer, CustomerGroup, Region, Interaction, Supplier
from rest_framework.authtoken.models import Token
from core.auxiliar import AdminBase
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'email', 'website')
    search_fields = ('name', 'city', 'state', 'email', 'website')
    readonly_fields = ('owner_token',)

    def owner_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj.owner)
        return token.key

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
@admin.register(Customer)
class CustomerAdmin(AdminBase):
    list_display = ('name', 'whatsapp','email', 'score')
    search_fields = ('name', 'whatsapp','email')

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