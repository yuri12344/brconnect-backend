# admin.py
from .models import WppConnectSession, TextMessage, ImageMessage, Campaign, VideoMessage
from core.auxiliar import AdminBase
from django.contrib import admin


@admin.register(WppConnectSession)
class WppConnectSessionAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')  # Adjust this according to your needs
    search_fields = ('id', 'company__name')  # Adjust this according to your needs

@admin.register(TextMessage)
class TextMessageAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')
    
@admin.register(ImageMessage)
class ImageMessageAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')    
    
@admin.register(VideoMessage)
class VideoMessageAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')
    
@admin.register(Campaign)
class CampaignAdmin(AdminBase):
    list_display = ('id', 'company', 'date_created')
    filter_horizontal = ('text_messages',)
    raw_id_fields = ('text_messages',) 
        
    
    
    
    
    
    
    
    
    
    