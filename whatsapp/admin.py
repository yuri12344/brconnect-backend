from django.contrib import admin
from .models import TextMessage, ImageMessage, WppConnectSession, Campaign

@admin.register(TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(ImageMessage)
class ImageMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(WppConnectSession)
class WppConnectSessionAdmin(admin.ModelAdmin):
    pass

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass
