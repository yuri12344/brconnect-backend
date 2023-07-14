# Generated by Django 4.2.2 on 2023-07-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='featured_products',
            field=models.ManyToManyField(blank=True, related_name='featured_categories', related_query_name='featured_category', to='products.product', verbose_name='Produtos Destaque'),
        ),
    ]