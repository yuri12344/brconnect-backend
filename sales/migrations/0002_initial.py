# Generated by Django 4.2.2 on 2023-07-03 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_initial'),
        ('users', '0001_initial'),
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='sales.coupon', verbose_name='Cupom'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='users.customer', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='coupon',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sales.coupon', verbose_name='Cupom'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.customer', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coupon',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='coupons', related_query_name='coupon', to='products.category', verbose_name='Categoria'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='collections',
            field=models.ManyToManyField(blank=True, related_name='coupons', related_query_name='coupon', to='sales.collection', verbose_name='Coleção'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='coupons', related_query_name='coupon', to='products.product', verbose_name='Produto'),
        ),
        migrations.AddField(
            model_name='collectionproduct',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.collection', verbose_name='Collection'),
        ),
        migrations.AddField(
            model_name='collectionproduct',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_products', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='collectionproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Produto'),
        ),
        migrations.AddField(
            model_name='collection',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='collections', to='products.category', verbose_name='Categorias'),
        ),
        migrations.AddField(
            model_name='collection',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='collection',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='collections', related_query_name='collection', through='sales.CollectionProduct', to='products.product', verbose_name='Produtos'),
        ),
    ]
