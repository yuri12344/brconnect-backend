from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefone deve ser inserido no formato correto: '+554187941579'. Até 15 digitos."
)

class Company(models.Model):
    """
    A Company represents a company.
    """
    INDUSTRY_CHOICES = [
        ('beauty', 'Beleza'),
        ('ecommerce', 'E-commerce'),
        ('education', 'Educação'),
        ('finance', 'Finanças'),
        ('food', 'Alimentação'),
        ('health', 'Saúde'),
        ('manufacturing', 'Manufatura'),
        ('other', 'Outro'),
        ('retail', 'Varejo'),
        ('services', 'Serviços'),
        ('tech', 'Tecnologia'),
    ]
    EMPLOYEE_COUNT_CHOICES = [
        (1, '1-10'),
        (2, '11-50'),
        (3, '51-200'),
        (4, '201-500'),
        (5, '501-1000'),
        (6, '1001-5000'),
        (7, '5001-10,000'),
        (8, '10,001+'),
    ]
    name                    = models.CharField(max_length=255, verbose_name="Nome", blank=True, null=True)
    street                  = models.CharField(max_length=255, verbose_name="Rua", blank=True, null=True)
    city                    = models.CharField(max_length=255, verbose_name="Cidade", blank=True, null=True)
    state                   = models.CharField(max_length=255, verbose_name="Estado", blank=True, null=True)
    zip_code                = models.CharField(max_length=255, verbose_name="CEP", blank=True, null=True)
    phone                   = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Numero de telefone")
    email                   = models.EmailField(max_length=255, verbose_name="Email", blank=True, null=True)
    website                 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Website")
    description             = models.TextField(verbose_name="Descrição", blank=True, null=True)
    owner                   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company', verbose_name="Criador")
    date_created            = models.DateTimeField(auto_now_add=True, verbose_name="Data Criação")
    chave_pix               = models.CharField(max_length=255, verbose_name="Chave Pix", blank=True, null=True)
    date_updated            = models.DateTimeField(auto_now=True, verbose_name="Data Atualização")
    cnpj                    = models.CharField(max_length=255, verbose_name="CNPJ", blank=True, null=True)
    logo                    = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logo")
    industry                = models.CharField(max_length=255, choices=INDUSTRY_CHOICES, blank=True, null=True, verbose_name="Indústria")
    order_expiration_days   = models.PositiveIntegerField(default=7, verbose_name="Dias para expiração do pedido não pago e não enviado")
    employee_count          = models.IntegerField(choices=EMPLOYEE_COUNT_CHOICES, blank=True, null=True, verbose_name="Quantidade de Funcionários")
    whatsapp_service        = models.CharField(max_length=255, choices=[('wppconnect', 'WppConnect'), ('baileys', 'Baileys')], default='wppconnect')

    class Meta:
        db_table = 'companies'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name

class Customer(models.Model):
    """
    A Customer represents a customer.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name                = models.CharField(max_length=255, verbose_name="Name")
    whatsapp            = models.CharField(max_length=20, null=True, blank=True, verbose_name="WhatsApp Number")
    email               = models.EmailField(max_length=255, null=True, blank=True, verbose_name="Email")    
    street              = models.CharField(max_length=255, null=True, blank=True, verbose_name="Street")
    state               = models.CharField(max_length=255, null=True, blank=True, verbose_name="State")
    city                = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    zip                 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Zip Code")
    phone               = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Phone Number") # validators should be a list
    birthday            = models.DateField(null=True, blank=True, verbose_name="Birthday")
    company             = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='customers', related_query_name='customer', verbose_name="Company"
    )
    date_created        = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    score               = models.IntegerField(default=0, verbose_name="Score")
    age                 = models.IntegerField(null=True, blank=True, verbose_name="Idade")
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="Gênero")
    whatsapp            = models.CharField(max_length=20, null=True, blank=True, verbose_name="WhatsApp Number")
    interaction_history = models.TextField(null=True, blank=True, verbose_name="Histórico de Interações")
    favorite_product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='loved_by', verbose_name="Produto Favorito"
    )
    purchase_history    = models.ManyToManyField(
        'sales.Order', related_name='purchasing_customers', blank=True, verbose_name="Histórico de Pedidos"
    )
    preferences = models.ManyToManyField('products.Product', blank=True, verbose_name="Preferências de Produto")

    class Meta:
        db_table = 'customers'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        unique_together = ('email', 'company',)  # Email should be unique per company

    def __str__(self):
        return self.name

    def calculate_score(self):
        self.score = self.interactions.aggregate(total_score=models.Sum('score'))['total_score'] or 0
        self.save()
    
    @property
    def interaction_history(self):
        return "\n".join(interaction.description for interaction in self.interactions.all())

    
class CustomerGroup(models.Model):
    """
    A CustomerGroup represents a group of customers.
    """
    name        = models.CharField(max_length=50, verbose_name="Nome do Grupo")
    customers   = models.ManyToManyField(Customer, related_name='groups', blank=True, verbose_name="Clientes")
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='groups', verbose_name="Empresa")

    class Meta:
        db_table = 'customer_groups'
        verbose_name = "Grupos de cliente"
        verbose_name_plural = "Grupos de clientes"

    def __str__(self):
        return self.name


class Interaction(models.Model):
    name        = models.CharField(max_length=255, verbose_name="Nome", default="Interação")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    date        = models.DateTimeField(auto_now_add=True, verbose_name="Data da Interação")
    score       = models.IntegerField(verbose_name="Pontuação", default=5)
    customers   = models.ManyToManyField(Customer, related_name='interactions', verbose_name="Clientes", blank=True)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interactions', verbose_name="Empresa")

    class Meta:
        db_table = 'interactions'
        verbose_name = "Interação"
        verbose_name_plural = "Interações"

    def __str__(self):
        return f'Interação {self.name}'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
