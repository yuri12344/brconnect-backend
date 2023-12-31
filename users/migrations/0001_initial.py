# Generated by Django 4.2.2 on 2023-07-18 01:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rua')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='Estado')),
                ('zip_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='CEP')),
                ('phone', models.CharField(blank=True, max_length=17, null=True, verbose_name='Numero de telefone')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('chave_pix', models.CharField(blank=True, max_length=255, null=True, verbose_name='Chave Pix')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Data Atualização')),
                ('cnpj', models.CharField(blank=True, max_length=255, null=True, verbose_name='CNPJ')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/', verbose_name='Logo')),
                ('industry', models.CharField(blank=True, choices=[('beauty', 'Beleza'), ('ecommerce', 'E-commerce'), ('education', 'Educação'), ('finance', 'Finanças'), ('food', 'Alimentação'), ('health', 'Saúde'), ('manufacturing', 'Manufatura'), ('other', 'Outro'), ('retail', 'Varejo'), ('services', 'Serviços'), ('tech', 'Tecnologia')], max_length=255, null=True, verbose_name='Indústria')),
                ('order_expiration_days', models.PositiveIntegerField(default=7, verbose_name='Dias para expiração do pedido não pago e não enviado')),
                ('employee_count', models.IntegerField(blank=True, choices=[(1, '1-10'), (2, '11-50'), (3, '51-200'), (4, '201-500'), (5, '501-1000'), (6, '1001-5000'), (7, '5001-10,000'), (8, '10,001+')], null=True, verbose_name='Quantidade de Funcionários')),
                ('whatsapp_service', models.CharField(choices=[('wppconnect', 'WppConnect'), ('baileys', 'Baileys')], default='wppconnect', max_length=255)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True, verbose_name='WhatsApp')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Telefone deve ser inserido no formato correto: '+554187941579'. Até 15 digitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numero de telefone')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Logradouro')),
                ('number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Número')),
                ('complement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('neighborhood', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro')),
                ('zip', models.CharField(blank=True, max_length=255, null=True, verbose_name='CEP')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='Estado')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('score', models.IntegerField(default=0, verbose_name='Score')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Idade')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1, null=True, verbose_name='Gênero')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa')),
                ('favorite_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loved_by', to='products.product', verbose_name='Produto Favorito')),
                ('preferences', models.ManyToManyField(blank=True, to='products.product', verbose_name='Preferências de Produto')),
                ('purchase_history', models.ManyToManyField(blank=True, related_name='purchasing_customers', to='sales.order', verbose_name='Histórico de Pedidos')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('regiao', models.CharField(max_length=255, verbose_name='Regiao')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Custo frete')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Região',
                'verbose_name_plural': 'Regiões',
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='Interação', max_length=255, verbose_name='Nome')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Data da Interação')),
                ('score', models.IntegerField(default=5, verbose_name='Pontuação')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa')),
                ('customers', models.ManyToManyField(blank=True, related_name='interactions', to='users.customer', verbose_name='Clientes')),
            ],
            options={
                'verbose_name': 'Interação',
                'verbose_name_plural': 'Interações',
                'db_table': 'interactions',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRegion',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('regiao', models.CharField(max_length=255, verbose_name='Regiao')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Custo frete')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Região',
                'verbose_name_plural': 'historical Regiões',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInteraction',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('name', models.CharField(default='Interação', max_length=255, verbose_name='Nome')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('date', models.DateTimeField(blank=True, editable=False, verbose_name='Data da Interação')),
                ('score', models.IntegerField(default=5, verbose_name='Pontuação')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Interação',
                'verbose_name_plural': 'historical Interações',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCustomerGroup',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='Nome do Grupo')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Grupos de cliente',
                'verbose_name_plural': 'historical Grupos de clientes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True, verbose_name='WhatsApp')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Telefone deve ser inserido no formato correto: '+554187941579'. Até 15 digitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numero de telefone')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Logradouro')),
                ('number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Número')),
                ('complement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('neighborhood', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro')),
                ('zip', models.CharField(blank=True, max_length=255, null=True, verbose_name='CEP')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='Estado')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('score', models.IntegerField(default=0, verbose_name='Score')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Idade')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1, null=True, verbose_name='Gênero')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.company', verbose_name='Empresa')),
                ('favorite_product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.product', verbose_name='Produto Favorito')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.region', verbose_name='Regiao')),
            ],
            options={
                'verbose_name': 'historical Cliente',
                'verbose_name_plural': 'historical Clientes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nome do Grupo')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', verbose_name='Empresa')),
                ('customers', models.ManyToManyField(blank=True, related_name='groups', to='users.customer', verbose_name='Clientes')),
            ],
            options={
                'verbose_name': 'Grupos de cliente',
                'verbose_name_plural': 'Grupos de clientes',
                'db_table': 'customer_groups',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.region', verbose_name='Regiao'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('phone', 'company')},
        ),
    ]
