# Generated by Django 4.2.2 on 2023-07-06 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0004_rename_whats_api_provider_wppconnectsession_whatsapp_api_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wppconnectsession',
            old_name='session_name',
            new_name='whatsapp_api_session',
        ),
    ]
