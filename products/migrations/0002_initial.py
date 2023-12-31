# Generated by Django 4.2.2 on 2023-07-18 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Produto'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalproductimage',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalproductimage',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproductimage',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.product', verbose_name='Produto'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcategoryrecommendation',
            name='category_a',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.category', verbose_name='Categoria A'),
        ),
        migrations.AddField(
            model_name='historicalcategoryrecommendation',
            name='category_b',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.category', verbose_name='Categoria B'),
        ),
        migrations.AddField(
            model_name='historicalcategoryrecommendation',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalcategoryrecommendation',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoryrecommendation',
            name='category_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations_as_category_a', to='products.category', verbose_name='Categoria A'),
        ),
        migrations.AddField(
            model_name='categoryrecommendation',
            name='category_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations_as_category_b', to='products.category', verbose_name='Categoria B'),
        ),
        migrations.AddField(
            model_name='categoryrecommendation',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='categories', related_query_name='category', to='products.product', verbose_name='Produtos'),
        ),
    ]
