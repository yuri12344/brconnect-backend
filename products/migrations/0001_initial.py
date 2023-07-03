# Generated by Django 4.2.2 on 2023-07-03 18:14

import django.core.validators
from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('alias', models.CharField(max_length=255, verbose_name='Alias')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryAffinity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='affinity_images/')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Preço')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('stock', models.IntegerField(default=999, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Estoque')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Produto',
                'verbose_name_plural': 'historical Produtos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Preço')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('stock', models.IntegerField(default=999, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Estoque')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_secondary', models.URLField(blank=True, null=True, verbose_name='URL Secundaria')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Imagem')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Imagem do Produto',
                'verbose_name_plural': 'Imagens do Produto',
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='WhatsAppProductInfo',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='ID do produto no WhatsApp fornecido pela Meta')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do Produto no WhatsApp')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição do Produto no WhatsApp')),
                ('retailer_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Código do item')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link do Whatsapp')),
            ],
            options={
                'verbose_name': 'Produto no WhatsApp',
                'verbose_name_plural': 'Produtos no WhatsApp',
                'db_table': 'whatsapp_product_info',
            },
        ),
    ]
