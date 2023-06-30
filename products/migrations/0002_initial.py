# Generated by Django 4.2.2 on 2023-06-30 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='users.company', verbose_name='Empresa'),
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
            model_name='categoryaffinity',
            name='category1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affinities_as_category1', to='products.category'),
        ),
        migrations.AddField(
            model_name='categoryaffinity',
            name='category2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affinities_as_category2', to='products.category'),
        ),
        migrations.AddField(
            model_name='categoryaffinity',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_affinities', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='users.company', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='categories', related_query_name='category', to='products.product', verbose_name='Produtos'),
        ),
        migrations.AlterUniqueTogether(
            name='categoryaffinity',
            unique_together={('category1', 'category2')},
        ),
    ]