# Generated by Django 4.2.3 on 2023-09-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_historicalorder_status_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='status',
            field=models.CharField(choices=[('Enviado', 'Enviado'), ('Não enviado', 'Não enviado'), ('Recebido', 'Recebido')], default='Não enviado', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Enviado', 'Enviado'), ('Não enviado', 'Não enviado'), ('Recebido', 'Recebido')], default='Não enviado', verbose_name='Status'),
        ),
    ]
