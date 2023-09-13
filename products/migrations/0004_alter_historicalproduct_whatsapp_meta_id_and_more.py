# Generated by Django 4.2.3 on 2023-09-06 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_categoryrecommendation_recommendation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='whatsapp_meta_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='ID produto Meta'),
        ),
        migrations.AlterField(
            model_name='product',
            name='whatsapp_meta_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID produto Meta'),
        ),
    ]