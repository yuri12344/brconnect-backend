# Generated by Django 4.2.2 on 2023-07-18 01:40

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('payment_method', models.CharField(choices=[('D', 'Dinheiro'), ('C', 'Cartão'), ('B', 'Boleto'), ('P', 'Pix')], default='P', max_length=255, verbose_name='Metodo de pagamento')),
                ('paid', models.BooleanField(choices=[(True, 'Pago'), (False, 'Não pago')], default=False, verbose_name='Pago')),
                ('paid_at', models.DateTimeField(blank=True, editable=False, verbose_name='Pago em: ')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Pedido',
                'verbose_name_plural': 'historical Pedidos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductOrderItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Item do Pedido',
                'verbose_name_plural': 'historical Itens do Pedido',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('payment_method', models.CharField(choices=[('D', 'Dinheiro'), ('C', 'Cartão'), ('B', 'Boleto'), ('P', 'Pix')], default='P', max_length=255, verbose_name='Metodo de pagamento')),
                ('paid', models.BooleanField(choices=[(True, 'Pago'), (False, 'Não pago')], default=False, verbose_name='Pago')),
                ('paid_at', models.DateTimeField(auto_now_add=True, verbose_name='Pago em: ')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='ProductOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
            ],
            options={
                'verbose_name': 'Item do Pedido',
                'verbose_name_plural': 'Itens do Pedido',
                'db_table': 'product_order_items',
            },
        ),
    ]
