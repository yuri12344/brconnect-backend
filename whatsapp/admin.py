# admin.py
from .models import WppConnectSession
from core.auxiliar import AdminBase
from django.contrib import admin


@admin.register(WppConnectSession)
class WppConnectSessionAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')  # Adjust this according to your needs
    search_fields = ('id', 'company__name')  # Adjust this according to your needs
