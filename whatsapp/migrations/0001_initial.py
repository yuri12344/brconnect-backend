# Generated by Django 4.2.2 on 2023-07-03 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_messages', to='users.company')),
            ],
            options={
                'verbose_name': 'Texto',
                'verbose_name_plural': 'Textos',
            },
        ),
        migrations.CreateModel(
            name='ImageMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Imagem')),
                ('caption', models.CharField(max_length=200, verbose_name='Legenda')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_messages', to='users.company')),
            ],
            options={
                'verbose_name': 'Imagem',
                'verbose_name_plural': 'Imagens',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('status', models.IntegerField(choices=[(0, 'Não enviado'), (1, 'Enviando'), (2, 'Enviado'), (3, 'Erro')], default=0, verbose_name='Status')),
                ('schedule_type', models.CharField(choices=[('now', 'Enviar Agora'), ('scheduled', 'Agendar Envio'), ('daily', 'Enviar Diariamente'), ('weekly', 'Enviar Semanalmente'), ('monthly', 'Enviar Mensalmente')], default='now', max_length=10)),
                ('schedule_time', models.TimeField(blank=True, null=True)),
                ('schedule_day', models.IntegerField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='users.company')),
                ('image_messages', models.ManyToManyField(blank=True, related_name='campaigns', to='whatsapp.imagemessage')),
                ('text_messages', models.ManyToManyField(blank=True, related_name='campaigns', to='whatsapp.textmessage')),
            ],
        ),
    ]