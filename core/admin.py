from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from users.models import Company
from django.contrib import admin

class CompanyInline(admin.StackedInline):
    model = Company
    can_delete = False
    verbose_name_plural = 'company'

class UserAdmin(BaseUserAdmin):
    inlines = (CompanyInline,)
    readonly_fields = ('user_token',)

    def user_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if len(fieldsets) > 1 and 'user_token' not in fieldsets[1][1]['fields']:
            fieldsets[1][1]['fields'] += ('user_token',)
        return fieldsets

admin.site.unregister(User)
admin.site.register(User, UserAdmin)