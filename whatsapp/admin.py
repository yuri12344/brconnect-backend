from django.contrib import admin
from .models import TextMessage, ImageMessage, WppConnectSession, Campaign

admin.site.register(TextMessage)
admin.site.register(ImageMessage)
admin.site.register(WppConnectSession)
admin.site.register(Campaign)

