from django.contrib import admin
from .models import TextMessage, ImageMessage

admin.site.register(TextMessage)
admin.site.register(ImageMessage)
